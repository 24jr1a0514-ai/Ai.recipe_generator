import streamlit as st
from pathlib import Path
import json
import os

st.set_page_config(
    page_title="AI Recipe Generator",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

with open("assets/style.css", "r") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

st.sidebar.markdown("# 🍳 AI Recipe Generator")
st.sidebar.markdown("---")

mode = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📝 Recipe Generator",
        "🥗 Fridge Mode",
        "💚 Healthy Alternative",
        "💰 Budget Recipes",
        "⭐ Favorites",
        "📚 History",
        "ℹ️ About"
    ]
)

st.sidebar.markdown("---")
if st.sidebar.checkbox("🌙 Dark Mode"):
    st.markdown("""
    <style>
    .main { background-color: #1a1a1a; color: white; }
    </style>
    """, unsafe_allow_html=True)

pages = {
    "🏠 Home": "pages/Home",
    "📝 Recipe Generator": "pages/Recipe_Generator",
    "🥗 Fridge Mode": "pages/Fridge_Mode",
    "💚 Healthy Alternative": "pages/Healthy_Alternative",
    "💰 Budget Recipes": "pages/Budget_Recipes",
    "⭐ Favorites": "pages/Favorites",
    "📚 History": "pages/History",
    "ℹ️ About": "pages/About"
}

if mode in pages:
    page_path = pages[mode]
    spec = __import__('importlib.util').util.spec_from_file_location("page_module", f"{page_path}.py")
    module = __import__('importlib.util').util.module_from_spec(spec)
    spec.loader.exec_module(module)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Stats")
data_dir = Path("data")
if data_dir.exists():
    if (data_dir / "history.json").exists():
        with open(data_dir / "history.json") as f:
            history = json.load(f)
            st.sidebar.metric("Recipes Generated", len(history))
    
    if (data_dir / "favorites.json").exists():
        with open(data_dir / "favorites.json") as f:
            favorites = json.load(f)
            st.sidebar.metric("Favorites Saved", len(favorites))

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔗 Links")
col1, col2, col3 = st.sidebar.columns(3)
with col1:
    st.markdown("[GitHub](https://github.com)")
with col2:
    st.markdown("[Twitter](https://twitter.com)")
with col3:
    st.markdown("[LinkedIn](https://linkedin.com)")

st.sidebar.markdown("---")
st.sidebar.markdown("© 2024 AI Recipe Generator | Powered by Gemini AI")