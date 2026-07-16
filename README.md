# Ai.recipe_generator
AI Recipe Generator is a Streamlit-based web app powered by Google Gemini AI that creates personalized recipes from available ingredients, cuisine, diet, cooking time, and preferences. It also offers ingredient image analysis, healthy alternatives, budget-friendly recipes, recipe history, favorites, PDF export, and a modern user interface.

# 🍳 AI Recipe Generator

An intelligent recipe generation application powered by Google Gemini AI and built with Streamlit.

## Features

- **Recipe Generator**: Create recipes based on ingredients, cuisine, meal type, and dietary preferences
- **Fridge Mode**: Upload images of ingredients for AI to detect and suggest recipes
- **Healthy Alternatives**: Get healthier versions of your favorite recipes
- **Budget Recipes**: Generate affordable recipes within your budget
- **Multiple Recipe Types**: Festival, Kids Friendly, Weight Loss, High Protein, Vegetarian & Vegan
- **Recipe History**: Track all generated recipes
- **Favorites**: Save and manage favorite recipes
- **PDF Export**: Download recipes as PDF files
- **Dark/Light Mode**: Customizable theme
- **Responsive Design**: Works on desktop and mobile devices

## Installation

### Prerequisites
- Python 3.12+
- Google Gemini API Key

### Setup

1. Clone the repository
```bash
git clone https://github.com/24jr1a0514/AI_Recipe_Generator.git
cd AI_Recipe_Generator

Create virtual environment
Bash
Install dependencies
Bash
Create .env file
Bash
Create data directory
Bash
Run the application
Bash
Usage
Recipe Generator
Enter ingredients, cuisine type, meal type, and other preferences
AI generates complete recipes with nutritional information
Fridge Mode
Upload an image of ingredients
AI detects available ingredients and suggests recipes
Healthy Alternative
Enter or upload a recipe
Get a healthier version with nutritional comparisons
Budget Recipes
Set your budget
Get affordable recipes within your price range
Favorites & History
Save recipes as favorites
View all previously generated recipes
Download recipes as PDF
Project Structure
AI_Recipe_Generator/
├── app.py                      # Main application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore file
├── assets/
│   └── style.css              # Custom CSS styling
├── pages/
│   ├── Home.py                # Homepage
│   ├── Recipe_Generator.py    # Main recipe generator
│   ├── Fridge_Mode.py         # Image-based ingredient detection
│   ├── Healthy_Alternative.py # Healthy recipe suggestions
│   ├── Budget_Recipes.py      # Budget-based recipes
│   ├── Favorites.py           # Favorites management
│   ├── History.py             # Recipe history
│   └── About.py               # About page
├── utils/
│   ├── gemini_api.py          # Gemini API integration
│   ├── image_processing.py    # Image processing utilities
│   ├── pdf_generator.py       # PDF export functionality
│   ├── storage.py             # Local storage management
│   ├── prompts.py             # AI prompt templates
│   └── helpers.py             # Helper functions
└── data/
    ├── history.json           # Recipe history storage
    └── favorites.json         # Favorites storage

API Integration
This project uses Google Gemini AI API. Get your free API key from Google AI Studio.
Features Roadmap
[ ] Recipe ratings and reviews
[ ] Social sharing integration
[ ] Multi-language support
[ ] Recipe video tutorials
[ ] Meal planning
[ ] Nutritional analysis charts
[ ] Community recipes
License
MIT License - feel free to use this project for personal or commercial purposes.
Support
For issues and questions, please open an issue on GitHub.
Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
FILE: .env