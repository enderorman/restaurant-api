import json
from model import Meal, Ingredient

class FileService:
    def __init__(self):
        self.menuData = self.loadMenuFromFile()
        self.mealList = []
        self.ingredientList = []
        self.populateMealList()
        self.populateIngredientList()

    def loadMenuFromFile(self):
        try:
            with open('../menu.json', 'r') as f:
                menu_data = json.load(f)
            return menu_data
        except FileNotFoundError:
            print("Menu file not found.")
            return {}
        except json.JSONDecodeError:
            print("Error decoding JSON in menu file.")
            return {}

    def populateMealList(self):
        meals = self.menuData.get('meals', [])
        for meal in meals:
            self.mealList.append(self.parseMealFromData(meal))

    def parseMealFromData(self, mealData):
        id, name, ingredients = mealData.get('id'), mealData.get('name'), mealData.get('ingredients')
        return Meal(id, name, ingredients)

    def populateIngredientList(self):
        ingredients = self.menuData.get('ingredients', [])
        for ingredient in ingredients:
            self.ingredientList.append(self.parseIngredientFromData(ingredient))

    def parseIngredientFromData(self, ingredientData):
        name, groups, options = ingredientData.get('name'), ingredientData.get('groups'), ingredientData.get('options')
        return Ingredient(name, groups, options)