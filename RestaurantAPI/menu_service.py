import json
import random
from meal import Meal
from ingredient import Ingredient
from file_service import FileService
from collections import defaultdict

class MealAdapter:
    @staticmethod
    def to_dict(meal):
        if meal is None:
            return None
        return {
            "id": meal.id,
            "name": meal.name,
            "ingredients": meal.ingredients
        }

class MenuService:
    def __init__(self, fileService):
        self.fileService = fileService
        self.mealList = self.fileService.mealList
        self.ingredientList = self.fileService.ingredientList

    def listMeals(self, is_vegetarian=False, is_vegan=False):
        return [MealAdapter.to_dict(meal) for meal in self.mealList if self.filterMeal(meal, is_vegetarian, is_vegan)]

    def _filterMeal(self, meal, is_vegetarian, is_vegan):
        for ingredientData in meal.ingredients:
            ingredientName = ingredientData.get('name')
            ingredient = self.getIngredientNameGiven(ingredientName)
            if not (not is_vegetarian or self.isIngredientVegetarian(ingredient)) and (not is_vegan or self.isIngredientVegan(ingredient)):
                return False
        return True

    def _isIngredientVegetarian(self, ingredient):
        return 'vegetarian' in ingredient.groups

    def _isIngredientVegan(self, ingredient):
        return 'vegan' in ingredient.groups

    def _getIngredientNameGiven(self, ingredientName):
        for ingredient in self.ingredientList:
            if ingredient.name.lower() in ingredientName.lower():
                return ingredient
        return None

    def getMeal(self, mealID):
        meal = self.getMealByID(mealID)
        return MealAdapter.to_dict(meal)

    def _getMealByID(self, mealID):
        for meal in self.mealList:
            if meal.id == mealID:
                return meal
        return None

    def _calculateQualityScoreForMeal(self, meal_id, ingredients):
        meal = self.getMealByID(meal_id)
        ingredientScores = []
        ingredientDefaults = defaultdict(lambda: "high",
                                         {ingredient.lower(): quality for ingredient, quality in ingredients.items()})
        for ingredient in meal.ingredients:
            ingredientName = ingredient.get('name', None).lower()
            ingredientScore = self.getIngredientQuality(ingredientDefaults[ingredientName])
            ingredientScores.append(ingredientScore)
        overall_quality = sum(ingredientScores) / len(ingredientScores)
        return overall_quality

    def calculateQualityScore(self, meal_id, ingredients):
        overall_quality = self.calculateQualityScoreForMeal(meal_id, ingredients)
        qualityScore = {
            "quality": overall_quality
        }
        return qualityScore

    def _getIngredientQuality(self, quality):
        if quality == "high":
            return 30
        elif quality == "medium":
            return 20
        elif quality == "low":
            return 10
        else:
            raise ValueError("Invalid quality level")

    def _calculatePriceForMeal(self, meal_id, ingredients):
        ingredientDefaults = defaultdict(lambda: "high",
                                         {ingredient.lower(): quality for ingredient, quality in ingredients.items()})
        meal = self.getMealByID(meal_id)
        price = 0
        for ingredientData in meal.ingredients:
            ingredientName = ingredientData.get('name').lower()
            ingredient, quality = self.getIngredientNameGiven(ingredientName), ingredientDefaults[ingredientName]
            price += self.calculateIngredientPriceForMeal(meal, ingredient, quality)
        return price

    def calculatePrice(self, meal_id, ingredients):
        price = self.calculatePriceForMeal(meal_id, ingredients)
        return {
            "price": price
        }

    def _calculateExtraCost(self, quality):
        if quality == "high":
            return 0
        elif quality == "medium":
            return 0.05
        elif quality == 'low':
            return 0.10

    def _calculateIngredientPriceForMeal(self, meal, ingredient, quality):
        extraCost = self.calculateExtraCost(quality)
        quantity, quantity_type = self.getIngredientQuantityInfoForMeal(meal, ingredient)
        price_per_amount, per_amount = self.getIngredientInfoGivenQuality(ingredient, quality)
        if quantity_type == 'gram':
            return (price_per_amount * quantity) / 1000 + extraCost
        elif quantity_type == 'millilitre':
            return (price_per_amount * quantity) / 1000 + extraCost

    def _getIngredientInfoGivenQuality(self, ingredient, quality):
        for option in ingredient.options:
            optionQuality = option.get('quality')
            if optionQuality == quality:
                price = option.get('price')
                per_amount = option.get('per_amount')
                return price, per_amount

    def _getIngredientQuantityInfoForMeal(self, meal, ingredient):
        mealIngredients = meal.ingredients
        for ingredientData in mealIngredients:
            mealIngredientName = ingredientData.get('name')
            if ingredient.name in mealIngredientName:
                quantity, quantity_type = ingredientData.get('quantity'), ingredientData.get('quantity_type')
                return quantity, quantity_type


    def selectRandomMealWithBudget(self, budget=None):
        if budget == None:
            randomMeal = self.selectRandomMeal()
            randomIngredients = self.generateIngredientsWithRandomQualities(randomMeal.ingredients)
            return self.getMealInfo(randomMeal, randomIngredients)
        randomMeal = self.selectRandomMeal()
        randomIngredients = self.generateIngredientsWithRandomQualities(randomMeal.ingredients)
        while self.isMealPriceGreaterThanBudget(randomMeal, randomIngredients, budget):
            randomMeal = self.selectRandomMeal()
            randomIngredients = self.generateIngredientsWithRandomQualities(randomMeal.ingredients)
        return self.getMealInfo(randomMeal, randomIngredients)

    def _getMealInfo(self, meal, ingredients):
        meal_id = meal.id
        name = meal.name
        price, qualityScore = self.calculatePriceForMeal(meal_id, ingredients), self.calculateQualityScoreForMeal(meal_id, ingredients)
        ingredientLst = [{"name": ingredientName, "quality":ingredientQuality} for ingredientName, ingredientQuality in
                        ingredients.items()]
        return {
            'id': meal_id,
            'name': name,
            'price': price,
            'quality_score': qualityScore,
            'ingredients': ingredientLst
        }

    def _isMealPriceGreaterThanBudget(self, randomMeal, randomIngredients, budget):
        meal_id = randomMeal.id
        price = self.calculatePriceForMeal(meal_id, randomIngredients)
        return price > budget

    def _selectRandomMeal(self):
        return random.choice(self.mealList)

    def _selectRandomQuality(self):
        qualities = ['high', 'medium', 'low']
        return random.choice(qualities)

    def _generateIngredientsWithRandomQualities(self, mealIngredients):
        randomQualityIngredients = {}
        for ingredientData in mealIngredients:
            ingredientName = ingredientData.get('name')
            randomQualityIngredients[ingredientName] = self.selectRandomQuality()
        return randomQualityIngredients

    def search(self, text):
        for meal in self.mealList:
            mealName = meal.name.lower()
            if text.lower() in mealName:
                return MealAdapter.to_dict(meal)
        return None

    def findHighest(self, budget, is_vegetarian, is_vegan):
        mealChoices = []
        for meal in self.mealList:
            self.generateMealsBelowBudget(meal, {}, budget, 0, 0, mealChoices, is_vegetarian, is_vegan)
        if not len(mealChoices):
            return None
        highestQualityMealChoice = self.getHighestQualityMealFromMealChoices(mealChoices)
        meal, ingredientChoice = highestQualityMealChoice
        return self.getMealInfo(meal, ingredientChoice)

    def _generateMealsBelowBudget(self, meal, ingredientChoice, budget, cost, index, mealChoices, is_vegetarian=False, is_vegan=False):
        qualities = ["low", "medium", "high"]
        ingredients = meal.ingredients
        if cost > budget or not self.filterMeal(meal, is_vegetarian, is_vegan):
            return
        if index >= len(ingredients):
            mealChoices.append((meal, ingredientChoice))
            return
        for quality in qualities:
            ingredientName = ingredients[index].get('name')
            ingredient = self.getIngredientNameGiven(ingredientName)
            ingredientChoice[ingredientName] = quality
            cost += self.calculateIngredientPriceForMeal(meal, ingredient, quality)
            self.generateMealsBelowBudget(meal, ingredientChoice.copy(), budget, cost, index + 1, mealChoices, is_vegetarian, is_vegan)

    def _getHighestQualityMealFromMealChoices(self, mealChoices):
        maxQuality = 0
        highestQualityMealChoice = None
        for choice in mealChoices:
            meal, ingredientChoice = choice
            quality = self.calculateQualityScoreForMeal(meal.id, ingredientChoice)
            if quality > maxQuality:
                highestQualityMealChoice = choice
                maxQuality = quality
        return highestQualityMealChoice

    def findHighestOfMeal(self, meal_id, budget):
        mealChoices = []
        meal = self.getMealByID(meal_id)
        self.generateMealsBelowBudget(meal, {}, budget, 0, 0, mealChoices)
        if not len(mealChoices):
            return None
        highestQualityChoice = self.getHighestQualityMealFromMealChoices(mealChoices)
        meal, ingredientChoice = highestQualityChoice
        return self.getMealInfo(meal, ingredientChoice)














