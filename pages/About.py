import streamlit as st

st.set_page_config(page_title="About", layout="wide")

st.title("ℹ️ About AI Recipe Generator")

st.markdown("""
## Welcome to AI Recipe Generator

An intelligent, AI-powered application that helps you discover delicious recipes tailored to your preferences, dietary needs, and available ingredients.

---

## 🎯 Our Mission

To make cooking accessible, enjoyable, and personalized for everyone using advanced artificial intelligence technology.

---

## ✨ Key Features

### Recipe Generation
Create unique recipes based on:
- Ingredients you have
- Cuisine preferences
- Meal type
- Dietary requirements
- Available cooking time

### Smart Image Recognition
Upload photos of your ingredients and let AI detect what you have and suggest recipes.

### Healthy Alternatives
Transform your favorite recipes into healthier versions without sacrificing taste.

### Budget-Friendly Options
Find delicious recipes within your budget with cost breakdowns.

### Special Occasion Recipes
- Festival recipes
- Family-friendly meals
- Weight loss recipes
- High protein options
- Vegetarian & Vegan choices

### Recipe Management
- Save favorites
- Track recipe history
- Download as PDF
- Share recipes

---

## 🤖 Technology

Built with:
- **Streamlit**: Interactive web application framework
- **Google Gemini AI**: Advanced AI model for recipe generation
- **Python 3.12**: Modern Python programming
- **Pillow**: Image processing
- **ReportLab**: PDF generation

---

## 👥 User Guide

### Getting Started

1. **Choose your mode** from the navigation menu
2. **Provide your preferences** (ingredients, cuisine, dietary needs)
3. **Let AI generate** your perfect recipe
4. **Customize and enjoy** your personalized recipe

### Tips for Best Results

- Be specific about ingredients
- Provide clear images for Fridge Mode
- Save favorite recipes for future reference
- Use the PDF export for offline access
- Check the history to track your cooking journey

---

## 🔐 Privacy & Security

- Your API key is stored securely in `.env`
- Recipes are stored locally
- No data is sent to external servers (except Gemini API)
- Your data remains completely private

---

## 📊 Statistics

Track your cooking journey with:
- Total recipes generated
- Favorite recipes saved
- Recipe history
- Dietary preference insights

---

## 🎓 How AI Works

The application uses Google's Gemini 2.5 Flash model to:
- Understand your preferences
- Generate creative recipes
- Analyze ingredient photos
- Suggest healthy alternatives
- Provide nutritional information
- Create budget-friendly options

---

## 💡 Tips & Tricks

- **Multiple Cuisines**: Mix cuisines for fusion recipes
- **Dietary Mix**: Combine dietary preferences creatively
- **Budget Planning**: Set realistic budgets for meal planning
- **Image Quality**: Use clear, well-lit photos for best results
- **Favorites**: Build your personal recipe collection

---

## 🐛 Troubleshooting

### Recipe not generating?
- Check your internet connection
- Verify API key is correct
- Ensure ingredients are specified

### Image not recognized?
- Use clear, well-lit photos
- Include ingredients clearly
- Try different angles

### PDF download not working?
- Check file permissions
- Use a supported browser
- Try downloading again

---

## 📞 Support

For issues or suggestions:
1. Check the troubleshooting section above
2. Verify your setup follows the README
3. Ensure Google API key is valid

---

## 🚀 Roadmap

Planned features:
- [ ] Recipe ratings system
- [ ] Social sharing integration
- [ ] Meal planning calendar
- [ ] Nutritional analytics charts
- [ ] Community recipe sharing
- [ ] Multi-language support
- [ ] Video tutorials
- [ ] Recipe video generation

---

## 📜 License

MIT License - Feel free to use, modify, and distribute.

---

## 🙏 Acknowledgments

- Google Gemini AI for powerful recipe generation
- Streamlit for the interactive framework
- Python community for excellent libraries
- You, for using our app!

---

## 📧 Contact & Feedback

Your feedback helps us improve! Share your thoughts about features you'd like to see.

---

<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; margin-top: 2rem;">
    <h3>Happy Cooking! 👨‍🍳</h3>
    <p>Create amazing recipes with AI</p>
    <p style="font-size: 0.9rem; margin-top: 1rem;">© 2024 AI Recipe Generator | Powered by Google Gemini AI</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

with st.expander("📋 Frequently Asked Questions"):
    st.markdown("""
    **Q: How accurate is the ingredient detection?**
    A: The AI provides good detection for common ingredients. Accuracy improves with clear, well-lit images.
    
    **Q: Can I use recipes for commercial purposes?**
    A: Yes, the recipes generated are yours to use as you wish.
    
    **Q: How do I export recipes?**
    A: Click the "Download PDF" button on any recipe to get a formatted PDF.
    
    **Q: Can I edit generated recipes?**
    A: Yes, treat them as templates and modify as needed!
    
    **Q: What if I don't have an API key?**
    A: Get a free API key from Google AI Studio (ai.google.dev).
    
    **Q: How many recipes can I generate?**
    A: Limited by your API quota. Free tier allows substantial usage.
    """)