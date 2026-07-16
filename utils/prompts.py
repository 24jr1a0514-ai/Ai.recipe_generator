class RecipePrompts:
    
    @staticmethod
    def get_recipe_generation_prompt(
        ingredients: list,
        cuisine: str,
        meal_type: str,
        dietary_preference: str,
        cooking_time: int,
        servings: int,
        spice_level: str
    ) -> str:
        return f"""
        Create a detailed recipe with the following specifications:
        
        Ingredients available: {', '.join(ingredients)}
        Cuisine type: {cuisine}
        Meal type: {meal_type}
        Dietary preference: {dietary_preference}
        Maximum cooking time: {cooking_time} minutes
        Number of servings: {servings}
        Spice level: {spice_level}
        
        Provide the response in this exact format:
        
        RECIPE NAME: [Name]
        
        DESCRIPTION: [2-3 sentence description]
        
        INGREDIENTS:
        [List each ingredient with quantity and unit]
        
        INSTRUCTIONS:
        [Number each step from 1 onwards]
        
        COOKING TIME: [Minutes]
        PREP TIME: [Minutes]
        
        NUTRITIONAL INFORMATION (per serving):
        Calories: [Number]
        Protein: [Grams]
        Carbohydrates: [Grams]
        Fat: [Grams]
        
        CHEF'S TIPS:
        [List 3-4 helpful tips]
        
        STORAGE INSTRUCTIONS:
        [Storage details and shelf life]
        """
    
    @staticmethod
    def get_fridge_mode_prompt(ingredients: str) -> str:
        return f"""
        Based on these detected ingredients: {ingredients}
        
        Generate 3 different recipe ideas that can be made with these ingredients.
        For each recipe provide:
        
        RECIPE [Number]: [Name]
        Ingredients needed: [List]
        Brief description: [Description]
        Why it works: [Why these ingredients work well together]
        Difficulty level: [Easy/Medium/Hard]
        Time required: [Minutes]
        """
    
    @staticmethod
    def get_healthy_alternative_prompt(original_recipe: str) -> str:
        return f"""
        Analyze this recipe and provide a healthier version:
        
        {original_recipe}
        
        Provide:
        1. HEALTHIER SUBSTITUTIONS: [List ingredient swaps]
        2. COOKING METHOD IMPROVEMENTS: [How to modify preparation]
        3. NUTRITIONAL COMPARISON: [Original vs Healthy version]
        4. HEALTHIER RECIPE: [Complete healthier recipe]
        5. HEALTH BENEFITS: [Why this version is healthier]
        6. ESTIMATED CALORIE REDUCTION: [Percentage/amount]
        """
    
    @staticmethod
    def get_budget_recipe_prompt(budget: float, servings: int, preferences: str = "") -> str:
        cost_per_serving = budget / servings if servings > 0 else budget
        return f"""
        Create an affordable recipe within these constraints:
        
        Total Budget: ${budget}
        Servings: {servings}
        Cost per serving: ${cost_per_serving:.2f}
        Additional preferences: {preferences}
        
        Provide:
        1. RECIPE NAME: [Name]
        2. INGREDIENTS WITH COSTS: [List with estimated prices]
        3. TOTAL COST: [Breakdown]
        4. STEP-BY-STEP INSTRUCTIONS: [Detailed steps]
        5. COOKING & PREP TIME: [Times]
        6. NUTRITIONAL INFO: [Per serving]
        7. MONEY-SAVING TIPS: [How to reduce costs further]
        8. BULK BUYING SUGGESTIONS: [If applicable]
        """
    
    @staticmethod
    def get_festival_recipe_prompt(festival_name: str, preferences: str = "") -> str:
        return f"""
        Create a recipe perfect for {festival_name} celebration.
        
        Additional preferences: {preferences}
        
        Provide:
        1. RECIPE NAME: [Traditional/Modern name]
        2. FESTIVAL SIGNIFICANCE: [Why this dish for {festival_name}]
        3. INGREDIENTS: [Complete list]
        4. INSTRUCTIONS: [Detailed steps]
        5. SERVING SUGGESTIONS: [How to present]
        6. CELEBRATION TIPS: [Making it special]
        7. PREP TIMELINE: [When to prepare each part]
        8. STORAGE: [How to store leftovers]
        """
    
    @staticmethod
    def get_kids_recipe_prompt(preferences: str = "") -> str:
        return f"""
        Create a kid-friendly recipe that's nutritious and fun.
        
        Preferences: {preferences}
        
        Must include:
        1. RECIPE NAME: [Fun, appealing name]
        2. WHY KIDS LOVE IT: [Appeal factors]
        3. INGREDIENTS: [Common, kid-friendly ingredients]
        4. INSTRUCTIONS: [Simple, easy-to-follow steps]
        5. FUN FACTOR: [Ways to make it interactive/fun]
        6. NUTRITIONAL VALUE: [What kids get from it]
        7. ALLERGY INFORMATION: [Common allergens to watch for]
        8. SERVING IDEAS: [Creative presentations]
        """
    
    @staticmethod
    def get_weight_loss_recipe_prompt(calories: int, preferences: str = "") -> str:
        return f"""
        Create a weight loss-friendly recipe under {calories} calories.
        
        Preferences: {preferences}
        
        Focus on:
        1. RECIPE NAME: [Name]
        2. INGREDIENTS: [High protein, low calorie options]
        3. INSTRUCTIONS: [Detailed steps]
        4. EXACT CALORIES: [Per serving breakdown]
        5. MACRO BREAKDOWN: [Protein/Carbs/Fat ratio]
        6. SATIETY FACTOR: [Why it keeps you full]
        7. PREP TIPS: [Meal prep friendly]
        8. MODIFICATIONS: [Ways to reduce calories further]
        """
    
    @staticmethod
    def get_high_protein_recipe_prompt(protein_grams: int, preferences: str = "") -> str:
        return f"""
        Create a high-protein recipe with at least {protein_grams}g protein per serving.
        
        Preferences: {preferences}
        
        Include:
        1. RECIPE NAME: [Name]
        2. PROTEIN SOURCES: [List all protein ingredients]
        3. INGREDIENTS: [Complete list]
        4. INSTRUCTIONS: [Detailed steps]
        5. PROTEIN BREAKDOWN: [Amount per ingredient]
        6. TOTAL PROTEIN: [Per serving]
        7. MUSCLE-BUILDING BENEFITS: [Why it's good for muscle]
        8. POST-WORKOUT SUITABILITY: [Timing and benefits]
        """
    
    @staticmethod
    def get_vegetarian_vegan_recipe_prompt(diet_type: str, preferences: str = "") -> str:
        return f"""
        Create a {diet_type} recipe.
        
        Preferences: {preferences}
        
        Ensure:
        1. RECIPE NAME: [Name]
        2. ANIMAL PRODUCT CHECK: [Confirming no animal products if vegan]
        3. INGREDIENTS: [Only {diet_type} approved]
        4. INSTRUCTIONS: [Complete steps]
        5. PROTEIN ALTERNATIVES: [How to get sufficient protein]
        6. NUTRITIONAL COMPLETENESS: [All essential nutrients]
        7. TASTE & SATISFACTION: [Why it's delicious]
        8. VEGAN/VEGETARIAN TIPS: [Brand recommendations, substitutes]
        """