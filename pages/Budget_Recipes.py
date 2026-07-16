import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.gemini_api import GeminiRecipeGenerator
from utils.storage import RecipeStorage
from utils.helpers import ValidationHelper, FormatHelper
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Budget Recipes", layout="wide")

st.title("💰 Budget Recipes")
st.markdown("Delicious and affordable recipes within your budget")

try:
    recipe_generator = GeminiRecipeGenerator()
    storage = RecipeStorage()
except Exception as e:
    st.error(f"Error initializing services: {str(e)}")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    budget = st.number_input(
        "Total Budget ($)",
        min_value=1.0,
        max_value=100.0,
        value=20.0,
        step=1.0
    )

with col2:
    servings = st.number_input(
        "Number of Servings",
        min_value=1,
        max_value=10,
        value=4
    )

col3, col4 = st.columns(2)

with col3:
    cuisine = st.selectbox(
        "Cuisine Type",
        ["Any", "Italian", "Mexican", "Asian", "American", "Mediterranean"]
    )

with col4:
    dietary_pref = st.selectbox(
        "Dietary Preference",
        ["No Preference", "Vegetarian", "Vegan"]
    )

ingredients = st.text_area(
    "Available ingredients (optional)",
    placeholder="rice\nbeans\nvegetables",
    height=100
)

if st.button("💰 Generate Budget Recipes", use_container_width=True):
    is_valid, message = ValidationHelper.validate_budget(budget)
    is_valid_servings, servings_msg = ValidationHelper.validate_servings(servings)
    
    if not is_valid or not is_valid_servings:
        st.error(f"Error: {message or servings_msg}")
    else:
        with st.spinner("Finding affordable recipes..."):
            try:
                available_ingredients = [ing.strip() for ing in ingredients.split('\n') if ing.strip()]
                
                ingredients_str = f"Available ingredients: {', '.join(available_ingredients)}" if available_ingredients else ""
                
                prompt = f"""
                Create 2 affordable recipes with these constraints:
                
                Budget: ${budget:.2f}
                Servings: {servings}
                Cost per serving: ${budget/servings:.2f}
                Cuisine: {cuisine}
                Dietary: {dietary_pref}
                {ingredients_str}
                
                For each recipe provide:
                
                RECIPE NAME: [Name]
                
                INGREDIENTS WITH COSTS:
                [Item] - $[Cost]
                
                TOTAL COST: $[Amount]
                COST PER SERVING: $[Amount]
                
                INSTRUCTIONS:
                [Step by step]
                
                COOKING TIME: [Minutes]
                PREP TIME: [Minutes]
                
                NUTRITIONAL INFO (per serving):
                Calories: [Amount]
                Protein: [Grams]
                
                MONEY-SAVING TIPS:
                [3-4 tips to reduce costs]
                
                BULK BUYING SUGGESTIONS:
                [How to save with bulk purchases]
                """
                
                response = recipe_generator.generate_recipe(prompt)
                
                st.markdown("---")
                st.subheader("🛒 Budget-Friendly Recipes")
                st.markdown(response)
                
                if st.button("⭐ Save to Favorites"):
                    recipe_data = {
                        'type': 'budget_recipe',
                        'budget': budget,
                        'servings': servings,
                        'content': response
                    }
                    if storage.add_to_favorites(recipe_data):
                        st.success("Saved!")
            
            except Exception as e:
                st.error(f"Error generating recipes: {str(e)}")
                logger.error(f"Error: {str(e)}")

st.markdown("---")

with st.expander("💡 Money-Saving Tips"):
    st.markdown("""
    - Buy seasonal ingredients
    - Use dried beans and lentils
    - Buy generic brands
    - Plan meals around sales
    - Reduce meat portions
    - Use leftover vegetables
    - Cook in batches
    - Minimize food waste
    """)