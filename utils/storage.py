import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class RecipeStorage:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.history_file = self.data_dir / "history.json"
        self.favorites_file = self.data_dir / "favorites.json"
        self._initialize_files()
    
    def _initialize_files(self):
        """Initialize JSON files if they don't exist"""
        for file_path in [self.history_file, self.favorites_file]:
            if not file_path.exists():
                with open(file_path, 'w') as f:
                    json.dump([], f)
    
    def save_to_history(self, recipe: Dict) -> bool:
        """Save recipe to history"""
        try:
            recipe['timestamp'] = datetime.now().isoformat()
            with open(self.history_file, 'r') as f:
                history = json.load(f)
            history.append(recipe)
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving to history: {str(e)}")
            return False
    
    def get_history(self) -> List[Dict]:
        """Get all recipes from history"""
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading history: {str(e)}")
            return []
    
    def clear_history(self) -> bool:
        """Clear all history"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump([], f)
            return True
        except Exception as e:
            logger.error(f"Error clearing history: {str(e)}")
            return False
    
    def add_to_favorites(self, recipe: Dict) -> bool:
        """Add recipe to favorites"""
        try:
            recipe['added_to_favorites'] = datetime.now().isoformat()
            with open(self.favorites_file, 'r') as f:
                favorites = json.load(f)
            
            if not any(fav.get('name') == recipe.get('name') for fav in favorites):
                favorites.append(recipe)
                with open(self.favorites_file, 'w') as f:
                    json.dump(favorites, f, indent=2)
                return True
            return False
        except Exception as e:
            logger.error(f"Error adding to favorites: {str(e)}")
            return False
    
    def get_favorites(self) -> List[Dict]:
        """Get all favorite recipes"""
        try:
            with open(self.favorites_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading favorites: {str(e)}")
            return []
    
    def remove_from_favorites(self, recipe_name: str) -> bool:
        """Remove recipe from favorites"""
        try:
            with open(self.favorites_file, 'r') as f:
                favorites = json.load(f)
            favorites = [fav for fav in favorites if fav.get('name') != recipe_name]
            with open(self.favorites_file, 'w') as f:
                json.dump(favorites, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error removing from favorites: {str(e)}")
            return False
    
    def search_history(self, query: str) -> List[Dict]:
        """Search history for recipes"""
        try:
            history = self.get_history()
            query_lower = query.lower()
            return [
                recipe for recipe in history
                if query_lower in recipe.get('name', '').lower() or
                   query_lower in recipe.get('cuisine', '').lower()
            ]
        except Exception as e:
            logger.error(f"Error searching history: {str(e)}")
            return []