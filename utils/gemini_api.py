import google.generativeai as genai
from typing import Optional
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class GeminiRecipeGenerator:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
    
    def generate_recipe(self, prompt: str) -> str:
        """Generate recipe using Gemini API"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating recipe: {str(e)}")
            raise
    
    def analyze_image(self, image_data) -> str:
        """Analyze image for ingredient detection"""
        try:
            response = self.model.generate_content([
                "Analyze this image and list all food ingredients you can identify. Be specific about quantities if visible.",
                image_data
            ])
            return response.text
        except Exception as e:
            logger.error(f"Error analyzing image: {str(e)}")
            raise
    
    def generate_healthy_alternative(self, recipe: str) -> str:
        """Generate healthier version of recipe"""
        try:
            prompt = f"""
            Analyze this recipe and provide a healthier alternative:
            
            {recipe}
            
            Provide:
            1. Healthier ingredient substitutions
            2. Cooking method modifications
            3. Nutritional improvements
            4. Step-by-step healthier version
            5. Calorie reduction estimate
            """
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating healthy alternative: {str(e)}")
            raise
    
    def generate_budget_recipe(self, budget: float, servings: int) -> str:
        """Generate recipe within budget"""
        try:
            prompt = f"""
            Create an affordable recipe with the following constraints:
            - Total budget: ${budget}
            - Number of servings: {servings}
            - Cost per serving: ${budget/servings:.2f}
            
            Provide:
            1. Recipe name
            2. Ingredients with estimated costs
            3. Total cost breakdown
            4. Step-by-step instructions
            5. Cooking and prep time
            6. Nutritional information
            7. Money-saving tips
            """
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating budget recipe: {str(e)}")
            raise

    def generate_special_recipe(self, recipe_type: str, preferences: dict) -> str:
        """Generate special occasion recipes"""
        try:
            pref_str = "\n".join([f"- {k}: {v}" for k, v in preferences.items()])
            prompt = f"""
            Create a {recipe_type} recipe with the following preferences:
            
            {pref_str}
            
            Provide:
            1. Recipe name
            2. Description
            3. Complete ingredients list with quantities
            4. Step-by-step instructions
            5. Cooking and prep time
            6. Nutritional information
            7. Special notes for {recipe_type}
            8. Storage and serving suggestions
            """
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating {recipe_type} recipe: {str(e)}")
            raise