import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.storage import RecipeStorage
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="History", layout="wide")

st.title("📚 Recipe History")
st.markdown("All your previously generated recipes")

try:
    storage = RecipeStorage()
except Exception as e:
    st.error(f"Error initializing storage: {str(e)}")
    st.stop()

history = storage.get_history()

if not history:
    st.info("No recipes generated yet!")
else:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Recipes", len(history))
    
    with col2:
        search_query = st.text_input("🔍 Search history")
    
    with col3:
        sort_by = st.selectbox("Sort by", ["Date (Newest)", "Date (Oldest)", "Name"])
    
    with col4:
        if st.button("🗑️ Clear History"):
            if st.confirmation_dialog("Clear all history?"):
                storage.clear_history()
                st.success("History cleared!")
                st.rerun()
    
    filtered_history = history
    
    if search_query:
        filtered_history = storage.search_history(search_query)
    
    if sort_by == "Date (Oldest)":
        filtered_history = filtered_history
    elif sort_by == "Date (Newest)":
        filtered_history = reversed(filtered_history)
    elif sort_by == "Name":
        filtered_history = sorted(filtered_history, key=lambda x: x.get('name', ''))
    
    if not filtered_history:
        st.warning("No recipes match your search")
    else:
        for i, recipe in enumerate(filtered_history):
            with st.container():
                col_recipe, col_action = st.columns([4, 1])
                
                with col_recipe:
                    st.subheader(f"🍽️ {recipe.get('name', 'Recipe')}")
                    
                    col_meta1, col_meta2, col_meta3 = st.columns(3)
                    with col_meta1:
                        st.caption(f"Generated: {recipe.get('timestamp', 'N/A')[:10]}")
                    with col_meta2:
                        if recipe.get('cooking_time'):
                            st.caption(f"Cook time: {recipe['cooking_time']} min")
                    with col_meta3:
                        if recipe.get('nutrition'):
                            st.caption(f"Cal: {recipe['nutrition'].get('calories', 'N/A')}")
                
                with col_action:
                    if st.button("⭐ Save", key=f"save_{i}"):
                        if storage.add_to_favorites(recipe):
                            st.success("Added to favorites!")
                        else:
                            st.info("Already in favorites")
                
                if recipe.get('description'):
                    st.markdown(f"*{recipe['description']}*")
                
                with st.expander("View Full Recipe"):
                    if recipe.get('ingredients'):
                        st.markdown("**Ingredients:**")
                        for ing in recipe['ingredients']:
                            st.markdown(f"• {ing}")
                    
                    if recipe.get('instructions'):
                        st.markdown("**Instructions:**")
                        for j, instr in enumerate(recipe['instructions'], 1):
                            st.markdown(f"{j}. {instr}")
                
                st.markdown("---")