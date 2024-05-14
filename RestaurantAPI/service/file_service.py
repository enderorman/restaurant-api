import json
from model import Meal, Ingredient

class FileService:
    def __init__(self, file_path):
        self.menuData = self._loadMenuFromFile(file_path)
        self.mealList = []
        self.ingredientList = []
        self._populateMealList()
        self._populateIngredientList()

    def _loadMenuFromFile(self, file_path):
        try:
            with open(file_path, 'r') as f:
                menu_data = json.load(f)
            return menu_data
        except FileNotFoundError:
            print("Menu file not found.")
            return {}
        except json.JSONDecodeError:
            print("Error decoding JSON in menu file.")
            return {}

    def _populateMealList(self):
        meals = self.menuData.get('meals', [])
        for meal in meals:
            self.mealList.append(self._parseMealFromData(meal))

    def _parseMealFromData(self, mealData):
        id, name, ingredients = mealData.get('id'), mealData.get('name'), mealData.get('ingredients')
        return Meal(id, name, ingredients)

    def _populateIngredientList(self):
        ingredients = self.menuData.get('ingredients', [])
        for ingredient in ingredients:
            self.ingredientList.append(self._parseIngredientFromData(ingredient))

    def _parseIngredientFromData(self, ingredientData):
        name, groups, options = ingredientData.get('name'), ingredientData.get('groups'), ingredientData.get('options')
        return Ingredient(name, groups, options)