import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.gemini_api import GeminiRecipeGenerator
from utils.image_processing import ImageProcessor
from utils.storage import RecipeStorage
from utils.pdf_generator import PDFRecipeGenerator
from utils.helpers import RecipeParser
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Fridge Mode", layout="wide")

st.title("🥗 Fridge Mode")
st.markdown("Upload a photo of your ingredients and let AI suggest recipes")

try:
    recipe_generator = GeminiRecipeGenerator()
    storage = RecipeStorage()
    image_processor = ImageProcessor()
except Exception as e:
    st.error(f"Error initializing services: {str(e)}")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 Upload Image")
    uploaded_file = st.file_uploader(
        "Choose an image of your ingredients",
        type=["jpg", "jpeg", "png", "webp"]
    )

with col2:
    st.subheader("🍳 Recipe Options")
    cuisine = st.selectbox(
        "Preferred Cuisine",
        ["Any", "Italian", "Mexican", "Indian", "Chinese", "Thai", "Asian Fusion", "Mediterranean"]
    )
    
    diet_type = st.selectbox(
        "Dietary Preference",
        ["No Preference", "Vegetarian", "Vegan", "Gluten-Free"]
    )

if uploaded_file is not None:
    if st.button("🔍 Analyze Ingredients", use_container_width=True):
        if not image_processor.validate_image(uploaded_file):
            st.error("Invalid image format. Please upload JPG, PNG, or WEBP")
        else:
            with st.spinner("Analyzing image..."):
                try:
                    st.image(uploaded_file, caption="Your ingredients", use_column_width=True)
                    
                    ingredients_text = recipe_generator.analyze_image(uploaded_file)
                    st.success("✓ Ingredients detected!")
                    
                    st.subheader("Detected Ingredients:")
                    st.markdown(ingredients_text)
                    
                    if st.button("🍳 Generate Recipes", use_container_width=True):
                        with st.spinner("Creating recipe suggestions..."):
                            prompt = f"""
                            Based on these detected ingredients:
                            {ingredients_text}
                            
                            Preferred cuisine: {cuisine}
                            Dietary preference: {diet_type}
                            
                            Generate 3 different recipes that can be made:
                            
                            For each recipe provide:
                            RECIPE NAME: [Name]
                            INGREDIENTS NEEDED: [List with quantities]
                            COOKING TIME: [Minutes]
                            DIFFICULTY: [Easy/Medium/Hard]
                            DESCRIPTION: [Why these ingredients work well]
                            
                            Instructions:
                            [Step by step]
                            
                            NUTRITIONAL INFO:
                            Calories: [Amount]
                            Protein: [Grams]
                            """
                            
                            response = recipe_generator.generate_recipe(prompt)
                            
                            st.markdown("---")
                            st.subheader("🍽️ Suggested Recipes")
                            st.markdown(response)
                
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")
                    logger.error(f"Image processing error: {str(e)}")

st.markdown("---")

st.info("""
💡 **Tips for best results:**
- Use clear, well-lit photos
- Include multiple angles if possible
- Show ingredients clearly
- Include fresh and pantry items
""")