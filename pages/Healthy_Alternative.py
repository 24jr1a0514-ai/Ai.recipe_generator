import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.gemini_api import GeminiRecipeGenerator
from utils.storage import RecipeStorage
from utils.image_processing import ImageProcessor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Healthy Alternative", layout="wide")

st.title("💚 Healthy Alternative")
st.markdown("Get healthier versions of your favorite recipes")

try:
    recipe_generator = GeminiRecipeGenerator()
    storage = RecipeStorage()
except Exception as e:
    st.error(f"Error initializing services: {str(e)}")
    st.stop()

tab1, tab2, tab3 = st.tabs(["📝 Enter Recipe", "📷 Upload Image", "📚 From History"])

with tab1:
    st.subheader("Enter Recipe Details")
    
    recipe_name = st.text_input("Recipe Name")
    
    recipe_text = st.text_area(
        "Paste the recipe or describe it",
        height=250,
        placeholder="Ingredients:\n1. Butter\n2. Sugar\n\nInstructions:\n1. Mix ingredients..."
    )
    
    health_focus = st.multiselect(
        "What health aspects to focus on?",
        ["Lower Calories", "Less Sugar", "Reduce Fat", "More Protein", "Gluten-Free", "Dairy-Free", "Low Sodium"]
    )
    
    if st.button("💚 Get Healthy Alternative", use_container_width=True):
        if not recipe_text:
            st.error("Please enter a recipe")
        else:
            with st.spinner("Creating healthier version..."):
                try:
                    focus_str = ", ".join(health_focus) if health_focus else "Overall health"
                    prompt = f"""
                    Make this recipe healthier focusing on: {focus_str}
                    
                    Original Recipe:
                    {recipe_text}
                    
                    Provide:
                    1. HEALTHIER INGREDIENT SUBSTITUTIONS:
                    [List each substitution with reason]
                    
                    2. COOKING METHOD IMPROVEMENTS:
                    [How to modify preparation]
                    
                    3. NUTRITIONAL COMPARISON:
                    Original vs Healthy version
                    
                    4. HEALTHIER RECIPE:
                    Ingredients: [With quantities]
                    Instructions: [Step by step]
                    
                    5. HEALTH BENEFITS:
                    [Why this is healthier]
                    
                    6. ESTIMATED IMPROVEMENTS:
                    - Calorie reduction: [Percentage]
                    - Sugar reduction: [Percentage]
                    - Fat reduction: [Percentage]
                    """
                    
                    response = recipe_generator.generate_recipe(prompt)
                    
                    st.markdown("---")
                    st.subheader("✨ Your Healthier Recipe")
                    st.markdown(response)
                    
                    if st.button("⭐ Save Healthy Version"):
                        healthy_recipe = {
                            'name': f"Healthy {recipe_name}",
                            'type': 'healthy_alternative',
                            'content': response
                        }
                        if storage.add_to_favorites(healthy_recipe):
                            st.success("Saved to favorites!")
                        else:
                            st.info("Already saved")
                
                except Exception as e:
                    st.error(f"Error creating healthy alternative: {str(e)}")
                    logger.error(f"Error: {str(e)}")

with tab2:
    st.subheader("Upload Recipe Photo")
    
    uploaded_file = st.file_uploader(
        "Upload a photo of your recipe",
        type=["jpg", "jpeg", "png"]
    )
    
    health_focus2 = st.multiselect(
        "Health focus",
        ["Lower Calories", "Less Sugar", "Reduce Fat", "More Protein"],
        key="health_focus2"
    )
    
    if uploaded_file and st.button("🔍 Analyze & Improve", use_container_width=True):
        with st.spinner("Analyzing recipe photo..."):
            try:
                st.image(uploaded_file, caption="Your recipe", use_column_width=True)
                
                prompt = f"""
                Analyze this food/dish in the image and provide a healthier version.
                Focus on: {", ".join(health_focus2) if health_focus2 else "Overall health"}
                
                Provide:
                1. What you see in the image
                2. Health concerns
                3. Healthier ingredients to use
                4. Cooking modifications
                5. Complete healthier recipe
                6. Nutritional improvements
                """
                
                response = recipe_generator.generate_recipe(prompt)
                st.markdown(response)
            
            except Exception as e:
                st.error(f"Error: {str(e)}")

with tab3:
    st.subheader("Make Your History Healthy")
    
    history = storage.get_history()
    if history:
        recipe_names = [r.get('name', 'Unnamed') for r in history]
        selected_recipe = st.selectbox("Select a recipe from history", recipe_names)
        
        if st.button("💚 Create Healthy Version", use_container_width=True):
            selected = next(r for r in history if r.get('name') == selected_recipe)
            
            with st.spinner("Creating healthier version..."):
                try:
                    prompt = f"""
                    Make this recipe healthier:
                    
                    {str(selected)}
                    
                    Provide improved version with:
                    1. Healthy substitutions
                    2. Modified cooking methods
                    3. Full healthy recipe
                    4. Nutritional comparison
                    """
                    
                    response = recipe_generator.generate_recipe(prompt)
                    st.markdown(response)
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    else:
        st.info("No recipes in history yet. Generate some recipes first!")