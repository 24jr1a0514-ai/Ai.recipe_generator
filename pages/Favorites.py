import streamlit as st
import sys
from pathlib import Path
import json

sys.path.append(str(Path(__file__).parent.parent))

from utils.storage import RecipeStorage
from utils.pdf_generator import PDFRecipeGenerator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Favorites", layout="wide")

st.title("⭐ Favorite Recipes")
st.markdown("Your saved favorite recipes")

try:
    storage = RecipeStorage()
except Exception as e:
    st.error(f"Error initializing storage: {str(e)}")
    st.stop()

favorites = storage.get_favorites()

if not favorites:
    st.info("📚 No favorite recipes yet! Start exploring and save your favorites.")
    st.markdown("""
    How to save favorites:
    1. Generate a recipe
    2. Click the ⭐ Add to Favorites button
    3. View all your favorites here
    """)
else:
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search favorites")
    
    with col2:
        sort_by = st.selectbox("Sort by", ["Date Added", "Name", "Type"])
    
    with col3:
        if st.button("🗑️ Clear All", use_container_width=True):
            if st.button("Confirm deletion"):
                storage.clear_history()
                st.success("Cleared!")
                st.rerun()
    
    filtered_favorites = favorites
    
    if search_query:
        filtered_favorites = [
            fav for fav in filtered_favorites
            if search_query.lower() in str(fav).lower()
        ]
    
    if not filtered_favorites:
        st.warning("No favorites match your search")
    else:
        for i, recipe in enumerate(filtered_favorites):
            with st.container():
                col_title, col_buttons = st.columns([3, 1])
                
                with col_title:
                    recipe_name = recipe.get('name', 'Recipe')
                    st.subheader(f"🍽️ {recipe_name}")
                    
                    if recipe.get('description'):
                        st.markdown(f"*{recipe['description']}*")
                
                with col_buttons:
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button("👁️", key=f"view_{i}"):
                            with st.expander("Recipe Details"):
                                st.json(recipe)
                    
                    with col_btn2:
                        if st.button("❌", key=f"delete_{i}"):
                            storage.remove_from_favorites(recipe_name)
                            st.success("Removed from favorites")
                            st.rerun()
                
                if recipe.get('ingredients'):
                    st.markdown("**Ingredients:**")
                    for ing in recipe.get('ingredients', [])[:5]:
                        st.markdown(f"• {ing}")
                    if len(recipe.get('ingredients', [])) > 5:
                        st.caption(f"... and {len(recipe['ingredients']) - 5} more")
                
                if recipe.get('nutrition'):
                    nut_col1, nut_col2, nut_col3 = st.columns(3)
                    with nut_col1:
                        st.metric("Calories", recipe['nutrition'].get('calories', 'N/A'))
                    with nut_col2:
                        st.metric("Protein", f"{recipe['nutrition'].get('protein', 'N/A')}g")
                    with nut_col3:
                        st.metric("Carbs", f"{recipe['nutrition'].get('carbs', 'N/A')}g")
                
                st.markdown("---")
        
        st.markdown(f"**Total favorites:** {len(filtered_favorites)}")