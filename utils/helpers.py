import re
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class RecipeParser:
    @staticmethod
    def parse_recipe_response(response_text: str) -> Dict:
        """Parse AI response into structured recipe data"""
        try:
            recipe = {
                'name': RecipeParser._extract_field(response_text, 'RECIPE NAME'),
                'description': RecipeParser._extract_field(response_text, 'DESCRIPTION'),
                'ingredients': RecipeParser._extract_list(response_text, 'INGREDIENTS'),
                'instructions': RecipeParser._extract_list(response_text, 'INSTRUCTIONS'),
                'nutrition': RecipeParser._extract_nutrition(response_text),
                'tips': RecipeParser._extract_list(response_text, "CHEF'S TIPS"),
                'storage': RecipeParser._extract_field(response_text, 'STORAGE'),
                'cooking_time': RecipeParser._extract_time(response_text, 'COOKING TIME'),
                'prep_time': RecipeParser._extract_time(response_text, 'PREP TIME'),
            }
            return recipe
        except Exception as e:
            logger.error(f"Error parsing recipe: {str(e)}")
            return {}
    
    @staticmethod
    def _extract_field(text: str, field_name: str) -> str:
        """Extract a field value from response text"""
        try:
            pattern = rf'{field_name}:\s*(.+?)(?=\n[A-Z]|\Z)'
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
            return ""
        except Exception as e:
            logger.error(f"Error extracting field {field_name}: {str(e)}")
            return ""
    
    @staticmethod
    def _extract_list(text: str, section_name: str) -> List[str]:
        """Extract a list from response text"""
        try:
            pattern = rf'{section_name}:\s*(.+?)(?=\n[A-Z]|\Z)'
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                content = match.group(1)
                items = [item.strip() for item in re.split(r'[\n•\-]', content)]
                return [item for item in items if item and len(item) > 2]
            return []
        except Exception as e:
            logger.error(f"Error extracting list {section_name}: {str(e)}")
            return []
    
    @staticmethod
    def _extract_nutrition(text: str) -> Dict:
        """Extract nutritional information"""
        try:
            nutrition = {}
            nutrition_patterns = {
                'calories': r'Calories:\s*(\d+)',
                'protein': r'Protein:\s*([\d.]+)',
                'carbs': r'Carbohydrates:\s*([\d.]+)',
                'fat': r'Fat:\s*([\d.]+)'
            }
            
            for key, pattern in nutrition_patterns.items():
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    nutrition[key] = match.group(1)
            
            return nutrition
        except Exception as e:
            logger.error(f"Error extracting nutrition: {str(e)}")
            return {}
    
    @staticmethod
    def _extract_time(text: str, time_type: str) -> str:
        """Extract cooking or prep time"""
        try:
            pattern = rf'{time_type}:\s*(\d+)\s*(?:minutes?|mins?)?'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
            return ""
        except Exception as e:
            logger.error(f"Error extracting time: {str(e)}")
            return ""

class ValidationHelper:
    @staticmethod
    def validate_ingredients(ingredients: List[str]) -> Tuple[bool, str]:
        """Validate ingredients list"""
        if not ingredients or len(ingredients) == 0:
            return False, "Please add at least one ingredient"
        if len(ingredients) > 50:
            return False, "Maximum 50 ingredients allowed"
        return True, "Valid"
    
    @staticmethod
    def validate_cooking_time(minutes: int) -> Tuple[bool, str]:
        """Validate cooking time"""
        if minutes <= 0:
            return False, "Cooking time must be greater than 0"
        if minutes > 1440:
            return False, "Cooking time cannot exceed 24 hours"
        return True, "Valid"
    
    @staticmethod
    def validate_servings(servings: int) -> Tuple[bool, str]:
        """Validate number of servings"""
        if servings <= 0:
            return False, "Servings must be greater than 0"
        if servings > 100:
            return False, "Maximum 100 servings allowed"
        return True, "Valid"
    
    @staticmethod
    def validate_budget(budget: float) -> Tuple[bool, str]:
        """Validate budget"""
        if budget <= 0:
            return False, "Budget must be greater than 0"
        if budget > 10000:
            return False, "Budget seems too high"
        return True, "Valid"

class FormatHelper:
    @staticmethod
    def format_time(minutes: int) -> str:
        """Format minutes to readable time"""
        if minutes < 60:
            return f"{minutes} minutes"
        hours = minutes // 60
        mins = minutes % 60
        if mins == 0:
            return f"{hours} hour{'s' if hours > 1 else ''}"
        return f"{hours}h {mins}m"
    
    @staticmethod
    def format_currency(amount: float) -> str:
        """Format currency"""
        return f"${amount:.2f}"
    
    @staticmethod
    def format_recipe_for_display(recipe: Dict) -> Dict:
        """Format recipe data for display"""
        formatted = recipe.copy()
        if recipe.get('cooking_time'):
            formatted['cooking_time_display'] = FormatHelper.format_time(int(recipe['cooking_time']))
        if recipe.get('prep_time'):
            formatted['prep_time_display'] = FormatHelper.format_time(int(recipe['prep_time']))
        return formatted