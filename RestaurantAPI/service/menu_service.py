import random
from collections import defaultdict
from model import Ingredient, Meal

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
        return [MealAdapter.to_dict(meal) for meal in self.mealList if self._filterMeal(meal, is_vegetarian, is_vegan)]

    def _filterMeal(self, meal, is_vegetarian, is_vegan):
        for ingredientData in meal.ingredients:
            ingredientName = ingredientData.get('name')
            ingredient = self._getIngredientNameGiven(ingredientName)
            if not ((not is_vegetarian or self._isIngredientVegetarian(ingredient)) and (not is_vegan or self._isIngredientVegan(ingredient))):
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
        meal = self._getMealByID(mealID)
        return MealAdapter.to_dict(meal) if meal is not None else None

    def _getMealByID(self, mealID):
        for meal in self.mealList:
            if meal.id == mealID:
                return meal
        return None

    def _calculateQualityScoreForMeal(self, meal_id, ingredients):
        meal = self._getMealByID(meal_id)
        ingredientScores = []
        ingredientDefaults = defaultdict(lambda: "high",
                                         {ingredient.lower(): quality for ingredient, quality in ingredients.items()})
        for ingredient in meal.ingredients:
            ingredientName = ingredient.get('name', None).lower()
            ingredientScore = self._getIngredientQuality(ingredientDefaults[ingredientName])
            ingredientScores.append(ingredientScore)
        overall_quality = sum(ingredientScores) / len(ingredientScores)
        return round(overall_quality, 2)

    def calculateQualityScore(self, meal_id, ingredients):
        overall_quality = self._calculateQualityScoreForMeal(meal_id, ingredients)
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
        meal = self._getMealByID(meal_id)
        price = 0
        for ingredientData in meal.ingredients:
            ingredientName = ingredientData.get('name').lower()
            ingredient, quality = self._getIngredientNameGiven(ingredientName), ingredientDefaults[ingredientName]
            price += self._calculateIngredientPriceForMeal(meal, ingredient, quality)
        return round(price, 2)

    def calculatePrice(self, meal_id, ingredients):
        price = self._calculatePriceForMeal(meal_id, ingredients)
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
        extraCost = self._calculateExtraCost(quality)
        quantity, quantity_type = self._getIngredientQuantityInfoForMeal(meal, ingredient)
        price_per_amount, per_amount = self._getIngredientInfoGivenQuality(ingredient, quality)
        if quantity_type == 'gram' and per_amount == 'kilogram':
            quantity /= 1000
        elif quantity_type == 'kilogram' and per_amount == 'gram':
            quantity *= 1000
        elif quantity_type == 'millilitre' and per_amount == 'litre':
            quantity /= 1000
        elif quantity_type == 'litre' and per_amount == 'millilitre':
            quantity *= 1000
        cost = (quantity * price_per_amount) + extraCost
        return round(cost, 2)

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
        mealChoices = []
        for meal in self.mealList:
            self._generateMealsBelowBudget(meal, {}, 0, 0, mealChoices, budget)
        if not len(mealChoices):
            return None
        randomChoice = random.choice(mealChoices)
        meal, ingredientChoice = randomChoice
        return self._getMealInfo(meal, ingredientChoice)

    def _getMealInfo(self, meal, ingredients):
        meal_id = meal.id
        name = meal.name
        price, qualityScore = self._calculatePriceForMeal(meal_id, ingredients), self._calculateQualityScoreForMeal(meal_id, ingredients)
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
        price = self._calculatePriceForMeal(meal_id, randomIngredients)
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
            randomQualityIngredients[ingredientName] = self._selectRandomQuality()
        return randomQualityIngredients

    def search(self, text):
        res = []
        for meal in self.mealList:
            mealName = meal.name.lower()
            if text.lower() in mealName:
                res.append(MealAdapter.to_dict(meal))
        return res

    def findHighest(self, budget, is_vegetarian, is_vegan):
        mealChoices = []
        for meal in self.mealList:
            self._generateMealsBelowBudget(meal, {}, 0, 0, mealChoices, budget, is_vegetarian, is_vegan)
        if not len(mealChoices):
            return None
        highestQualityMealChoice = self._getHighestQualityMealFromMealChoices(mealChoices)
        meal, ingredientChoice = highestQualityMealChoice
        return self._getMealInfo(meal, ingredientChoice)

    def _generateMealsBelowBudget(self, meal, ingredientChoice, cost, index, mealChoices, budget=None, is_vegetarian=False, is_vegan=False):
        qualities = ["low", "medium", "high"]
        ingredients = meal.ingredients
        if cost > budget or not self._filterMeal(meal, is_vegetarian, is_vegan):
            return
        if index >= len(ingredients):
            mealChoices.append((meal, ingredientChoice))
            return
        for quality in qualities:
            ingredientName = ingredients[index].get('name')
            ingredient = self._getIngredientNameGiven(ingredientName)
            ingredientChoice[ingredientName] = quality
            cost += self._calculateIngredientPriceForMeal(meal, ingredient, quality)
            self._generateMealsBelowBudget(meal, ingredientChoice.copy(), cost, index + 1, mealChoices, budget, is_vegetarian, is_vegan)

    def _getHighestQualityMealFromMealChoices(self, mealChoices):
        maxQuality = 0
        highestQualityMealChoice = None
        for choice in mealChoices:
            meal, ingredientChoice = choice
            quality = self._calculateQualityScoreForMeal(meal.id, ingredientChoice)
            if quality > maxQuality:
                highestQualityMealChoice = choice
                maxQuality = quality
        return highestQualityMealChoice

    def findHighestOfMeal(self, meal_id, budget):
        mealChoices = []
        meal = self._getMealByID(meal_id)
        self._generateMealsBelowBudget(meal, {}, 0, 0, mealChoices, budget)
        if not len(mealChoices):
            return None
        highestQualityChoice = self._getHighestQualityMealFromMealChoices(mealChoices)
        meal, ingredientChoice = highestQualityChoice
        return self._getMealInfo(meal, ingredientChoice)














