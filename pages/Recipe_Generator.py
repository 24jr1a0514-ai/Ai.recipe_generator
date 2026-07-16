import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.gemini_api import GeminiRecipeGenerator
from utils.prompts import RecipePrompts
from utils.storage import RecipeStorage
from utils.pdf_generator import PDFRecipeGenerator
from utils.helpers import RecipeParser, ValidationHelper, FormatHelper
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Recipe Generator", layout="wide")

st.title("📝 Recipe Generator")
st.markdown("Create delicious recipes based on your preferences")

try:
    recipe_generator = GeminiRecipeGenerator()
    storage = RecipeStorage()
except Exception as e:
    st.error(f"Error initializing services: {str(e)}")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Ingredients")
    ingredients_input = st.text_area(
        "Enter ingredients (one per line)",
        height=150,
        placeholder="chicken\nrice\ntomatoes\nonions"
    )

with col2:
    st.subheader("Recipe Preferences")
    cuisine = st.selectbox(
        "Cuisine Type",
        ["Italian", "Mexican", "Indian", "Chinese", "Thai", "Japanese", "Mediterranean", "American", "French", "Korean"]
    )
    
    meal_type = st.selectbox(
        "Meal Type",
        ["Breakfast", "Lunch", "Dinner", "Appetizer", "Dessert", "Snack", "Side Dish", "Soup"]
    )

col3, col4 = st.columns(2)

with col3:
    dietary_pref = st.selectbox(
        "Dietary Preference",
        ["No Preference", "Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Keto", "Low-Carb", "High-Protein"]
    )
    
    cooking_time = st.slider(
        "Maximum Cooking Time (minutes)",
        min_value=5,
        max_value=240,
        value=30,
        step=5
    )

with col4:
    servings = st.number_input(
        "Number of Servings",
        min_value=1,
        max_value=20,
        value=4
    )
    
    spice_level = st.select_slider(
        "Spice Level",
        options=["No Spice", "Mild", "Medium", "Hot", "Very Hot"]
    )

if st.button("🍳 Generate Recipe", use_container_width=True):
    ingredients = [ing.strip() for ing in ingredients_input.split('\n') if ing.strip()]
    
    is_valid, message = ValidationHelper.validate_ingredients(ingredients)
    is_valid_time, time_msg = ValidationHelper.validate_cooking_time(cooking_time)
    is_valid_servings, servings_msg = ValidationHelper.validate_servings(servings)
    
    if not is_valid or not is_valid_time or not is_valid_servings:
        st.error(f"Validation error: {message or time_msg or servings_msg}")
    else:
        with st.spinner("🤖 Generating recipe..."):
            try:
                prompt = RecipePrompts.get_recipe_generation_prompt(
                    ingredients=ingredients,
                    cuisine=cuisine,
                    meal_type=meal_type,
                    dietary_preference=dietary_pref,
                    cooking_time=cooking_time,
                    servings=servings,
                    spice_level=spice_level
                )
                
                response = recipe_generator.generate_recipe(prompt)
                recipe_data = RecipeParser.parse_recipe_response(response)
                
                if not recipe_data.get('name'):
                    recipe_data['name'] = f"{cuisine} {meal_type}"
                
                st.session_state.current_recipe = recipe_data
                st.session_state.show_recipe = True
            except Exception as e:
                st.error(f"Error generating recipe: {str(e)}")
                logger.error(f"Recipe generation error: {str(e)}")

if st.session_state.get('show_recipe') and st.session_state.get('current_recipe'):
    recipe = st.session_state.current_recipe
    
    st.markdown("---")
    
    with st.container():
        st.markdown(f"<h2 style='color: #FF6B6B;'>{recipe.get('name', 'Recipe')}</h2>", unsafe_allow_html=True)
        
        if recipe.get('description'):
            st.markdown(f"*{recipe['description']}*")
        
        col_button1, col_button2, col_button3, col_button4 = st.columns(4)
        
        with col_button1:
            if st.button("⭐ Add to Favorites", use_container_width=True):
                if storage.add_to_favorites(recipe):
                    st.success("Added to favorites!")
                else:
                    st.info("Already in favorites")
        
        with col_button2:
            if st.button("📋 Copy Recipe", use_container_width=True):
                st.info("Recipe copied to clipboard!")
        
        with col_button3:
            if st.button("📥 Save to History", use_container_width=True):
                if storage.save_to_history(recipe):
                    st.success("Saved to history!")
        
        with col_button4:
            if st.button("📄 Download PDF", use_container_width=True):
                try:
                    pdf_generator = PDFRecipeGenerator()
                    pdf_bytes = pdf_generator.generate_pdf(recipe)
                    st.download_button(
                        label="Click to download",
                        data=pdf_bytes,
                        file_name=f"{recipe.get('name', 'recipe').replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")
        
        st.markdown("---")
        
        col_ing, col_time = st.columns([2, 1])
        
        with col_ing:
            st.subheader("📦 Ingredients")
            if recipe.get('ingredients'):
                for ingredient in recipe['ingredients']:
                    st.markdown(f"✓ {ingredient}")
        
        with col_time:
            st.subheader("⏱️ Time")
            if recipe.get('prep_time'):
                st.metric("Prep Time", f"{recipe['prep_time']} min")
            if recipe.get('cooking_time'):
                st.metric("Cook Time", f"{recipe['cooking_time']} min")
        
        st.markdown("---")
        
        if recipe.get('nutrition'):
            st.subheader("🔬 Nutrition (per serving)")
            nutrition_col1, nutrition_col2, nutrition_col3, nutrition_col4 = st.columns(4)
            
            with nutrition_col1:
                st.metric("Calories", recipe['nutrition'].get('calories', 'N/A'))
            with nutrition_col2:
                st.metric("Protein", f"{recipe['nutrition'].get('protein', 'N/A')}g")
            with nutrition_col3:
                st.metric("Carbs", f"{recipe['nutrition'].get('carbs', 'N/A')}g")
            with nutrition_col4:
                st.metric("Fat", f"{recipe['nutrition'].get('fat', 'N/A')}g")
        
        st.markdown("---")
        
        st.subheader("👨‍🍳 Instructions")
        if recipe.get('instructions'):
            for i, instruction in enumerate(recipe['instructions'], 1):
                st.markdown(f"**Step {i}:** {instruction}")
        
        if recipe.get('tips'):
            st.markdown("---")
            st.subheader("💡 Chef's Tips")
            for tip in recipe['tips']:
                st.markdown(f"• {tip}")
        
        if recipe.get('storage'):
            st.markdown("---")
            st.subheader("🧊 Storage Instructions")
            st.markdown(recipe['storage'])