import sys
import unittest
from service import MenuService, FileService
class TestMenuService(unittest.TestCase):
    def setUp(self):
        #Specify file path as desired.
        file_path = "menu.json"
        self.menuService = MenuService(FileService(file_path))
    def testListMeals(self):
        params = [[False, False],
                  [True, False],
                  [True, True]]
        expectedMeals = [
            [
                {
                    "id": 1,
                    "name": "Rice and chicken bowl",
                    "ingredients": [
                        {"name": "Rice", "quantity": 120, "quantity_type": "gram"},
                        {"name": "Chicken", "quantity": 85, "quantity_type": "gram"}
                    ]
                },
                {
                    "id": 2,
                    "name": "Pasta with marinara sauce and vegetables",
                    "ingredients": [
                        {"name": "Pasta", "quantity": 115, "quantity_type": "gram"},
                        {
                            "name": "Marinara sauce",
                            "quantity": 120,
                            "quantity_type": "millilitre"
                        },
                        {"name": "Vegetables", "quantity": 240, "quantity_type": "gram"}
                    ]
                },
                {
                    "id": 3,
                    "name": "Grilled chicken with roasted vegetables",
                    "ingredients": [
                        {"name": "Chicken", "quantity": 85, "quantity_type": "gram"},
                        {"name": "Vegetables", "quantity": 240, "quantity_type": "gram"}
                    ]
                },
                {
                    "id": 4,
                    "name": "Beef stir-fry with rice",
                    "ingredients": [
                        {"name": "Beef", "quantity": 115, "quantity_type": "gram"},
                        {"name": "Rice", "quantity": 120, "quantity_type": "gram"},
                        {"name": "Vegetables", "quantity": 240, "quantity_type": "gram"}
                    ]
                },
                {
                    "id": 5,
                    "name": "Pork chops with mashed potatoes and gravy",
                    "ingredients": [
                        {"name": "Pork chops", "quantity": 115, "quantity_type": "gram"},
                        {
                            "name": "Mashed potatoes",
                            "quantity": 120,
                            "quantity_type": "gram"
                        },
                        {"name": "Gravy", "quantity": 120, "quantity_type": "millilitre"}
                    ]
                },
                {
                    "id": 6,
                    "name": "Grilled salmon with roasted asparagus",
                    "ingredients": [
                        {"name": "Salmon", "quantity": 85, "quantity_type": "gram"},
                        {"name": "Asparagus", "quantity": 240, "quantity_type": "gram"}
                    ]
                },
                {
                    "id": 7,
                    "name": "Shrimp scampi with linguine",
                    "ingredients": [
                        {"name": "Shrimp", "quantity": 115, "quantity_type": "gram"},
                        {"name": "Linguine", "quantity": 115, "quantity_type": "gram"},
                        {"name": "Butter", "quantity": 10, "quantity_type": "millilitre"},
                        {"name": "Garlic", "quantity": 10, "quantity_type": "gram"},
                        {"name": "White wine", "quantity": 60, "quantity_type": "millilitre"}
                    ]
                },
                {
                    "id": 8,
                    "name": "Vegetarian stir-fry with tofu",
                    "ingredients": [
                        {"name": "Tofu", "quantity": 115, "quantity_type": "gram"},
                        {"name": "Rice", "quantity": 120, "quantity_type": "gram"},
                        {"name": "Vegetables", "quantity": 240, "quantity_type": "gram"}
                    ]
                },
                {
                    "id": 9,
                    "name": "Fruit salad with mixed berries and yogurt",
                    "ingredients": [
                        {"name": "Mixed berries", "quantity": 240, "quantity_type": "gram"},
                        {"name": "Yogurt", "quantity": 120, "quantity_type": "millilitre"}
                    ]
                }
            ],
            [
                {
                    "id": 2,
                    "name": "Pasta with marinara sauce and vegetables",
                    "ingredients": [
                        {"name": "Pasta", "quantity": 115, "quantity_type": "gram"},
                        {
                            "name": "Marinara sauce",
                            "quantity": 120,
                            "quantity_type": "millilitre"
                        },
                        {"name": "Vegetables", "quantity": 240, "quantity_type": "gram"}
                    ]
                },
                {
                    "id": 8,
                    "name": "Vegetarian stir-fry with tofu",
                    "ingredients": [
                        {"name": "Tofu", "quantity": 115, "quantity_type": "gram"},
                        {"name": "Rice", "quantity": 120, "quantity_type": "gram"},
                        {"name": "Vegetables", "quantity": 240, "quantity_type": "gram"}
                    ]
                },
                {
                    "id": 9,
                    "name": "Fruit salad with mixed berries and yogurt",
                    "ingredients": [
                        {"name": "Mixed berries", "quantity": 240, "quantity_type": "gram"},
                        {"name": "Yogurt", "quantity": 120, "quantity_type": "millilitre"}
                    ]
                }
            ],
            [
                {
                    "id": 8,
                    "name": "Vegetarian stir-fry with tofu",
                    "ingredients": [
                        {"name": "Tofu", "quantity": 115, "quantity_type": "gram"},
                        {"name": "Rice", "quantity": 120, "quantity_type": "gram"},
                        {"name": "Vegetables", "quantity": 240, "quantity_type": "gram"}
                    ]
                }
            ]
        ]
        listMealsResult = [self.menuService.listMeals(param[0], param[1]) for param in params]
        self.assertListEqual(listMealsResult, expectedMeals)

    def testGetMeal(self):
        IDList = [0, 1, 2, 8, 20]
        expected = [None,
                    {
                        "id": 1,
                        "name": "Rice and chicken bowl",
                        "ingredients": [
                            {"name": "Rice", "quantity": 120, "quantity_type": "gram"},
                            {"name": "Chicken", "quantity": 85, "quantity_type": "gram"}
                        ]
                    },
                    {
                        "id": 2,
                        "name": "Pasta with marinara sauce and vegetables",
                        "ingredients": [
                            {"name": "Pasta", "quantity": 115, "quantity_type": "gram"},
                            {
                                "name": "Marinara sauce",
                                "quantity": 120,
                                "quantity_type": "millilitre"
                            },
                            {"name": "Vegetables", "quantity": 240, "quantity_type": "gram"}
                        ]
                    },
                    {
                        "id": 8,
                        "name": "Vegetarian stir-fry with tofu",
                        "ingredients": [
                            {"name": "Tofu", "quantity": 115, "quantity_type": "gram"},
                            {"name": "Rice", "quantity": 120, "quantity_type": "gram"},
                            {"name": "Vegetables", "quantity": 240, "quantity_type": "gram"}
                        ]
                    },
                    None
                    ]
        getMealResult = [self.menuService.getMeal(id) for id in IDList]
        self.assertListEqual(getMealResult, expected)

    def testCalculateQualityScore(self):
        testInputs = [
            {
                'meal_id': 1,
                'ingredients':{
                    'Rice':'low',
                    'Chicken':'high'
                }
            },
            {
                'meal_id': 4,
                'ingredients':{
                    'Beef':'high',
                    'Vegetables':'medium'
                    }
            },
            {
                'meal_id':7,
                'ingredients':{
                    'Shrimp':'high',
                    'Linguine':'low',
                    'White wine':'medium'
                }
            }
        ]
        calculateQualityScoreResults = [self.menuService.calculateQualityScore(input['meal_id'], input['ingredients'])
                                        for input in testInputs
                                        ]
        expected = [{'quality': 20}, {'quality': 26.67}, {'quality':24}]
        self.assertListEqual(calculateQualityScoreResults, expected)

    def testCalculatePrice(self):
        testInputs = [{
            'meal_id':1,
            'ingredients':{
                'Rice':'low',
                'Chicken':'high'
                }
            },
            {
            'meal_id':5,
            'ingredients':{
                'Mashed potatoes':'medium',
                'Gravy':'low'
                }
            },
            {
             'meal_id':7,
             'ingredients':{
                 'Shrimp':'low',
                 'Linguine':'high',
                 'Garlic':'medium',
                 'Butter':'low'
             }
            }
        ]
        calculatePriceResults = [self.menuService.calculatePrice(input['meal_id'], input['ingredients'])
                                        for input in testInputs
                                        ]
        expected = [
            {'price':1.13}, {'price':842.01}, {'price':4.11}
        ]
        self.assertListEqual(calculatePriceResults, expected)

    def testSelectRandomMealWithBudget(self):
        testInputs = [32.04, 43, 55, 100, 0.1]
        randomMeals = [self.menuService.selectRandomMealWithBudget(budget) for budget in testInputs]
        for i in range(len(testInputs)):
            if randomMeals[i] is not None:
                price = randomMeals[i].get('price')
                self.assertGreaterEqual(testInputs[i], price)

    def testSearch(self):
        testInputs = ["chick", "stir"]
        searchResults = [self.menuService.search(text) for text in testInputs]
        expected = [
            [
                {
                    "id": 1,
                    "name": "Rice and chicken bowl",
                    "ingredients": [
                        {"name": "Rice", "quantity": 120, "quantity_type": "gram"},
                        {"name": "Chicken", "quantity": 85, "quantity_type": "gram"}
                    ]
                },
                {
                    "id": 3,
                    "name": "Grilled chicken with roasted vegetables",
                    "ingredients": [
                        {"name": "Chicken", "quantity": 85, "quantity_type": "gram"},
                        {"name": "Vegetables", "quantity": 240, "quantity_type": "gram"}
                    ]
                }
            ],
            [
                {
                    "id": 4,
                    "name": "Beef stir-fry with rice",
                    "ingredients": [
                        {"name": "Beef", "quantity": 115, "quantity_type": "gram"},
                        {"name": "Rice", "quantity": 120, "quantity_type": "gram"},
                        {"name": "Vegetables", "quantity": 240, "quantity_type": "gram"}
                    ]
                },
                {
                    "id": 8,
                    "name": "Vegetarian stir-fry with tofu",
                    "ingredients": [
                        {"name": "Tofu", "quantity": 115, "quantity_type": "gram"},
                        {"name": "Rice", "quantity": 120, "quantity_type": "gram"},
                        {"name": "Vegetables", "quantity": 240, "quantity_type": "gram"}
                    ]
                }
            ]
        ]
        self.assertListEqual(searchResults, expected)
    def testFindHighest(self):
        testInputs = [
            {
                'budget':42.42,
                'is_vegetarian':True,
                'is_vegan':False
            },
            {
                'budget':1.15,
                'is_vegetarian':False,
                'is_vegan':False
            }
        ]
        findHighestResults = [self.menuService.findHighest(testInput['budget'],
                            testInput['is_vegetarian'], testInput['is_vegan']) for testInput in testInputs]

        for i in range(len(findHighestResults)):
            self.assertGreaterEqual(testInputs[i].get('budget'), findHighestResults[i].get('price'))
    def testFindHighestOfMeal(self):
        testInputs = [
            {
                'meal_id': 1,
                'budget': 2
            },
            {
                'meal_id': 7,
                'budget': 100
            },
            {
                'meal_id': 3,
                'budget': 20
            }
        ]
        findHighestResults = [self.menuService.findHighestOfMeal(testInput['meal_id'], testInput['budget']) for testInput in testInputs]
        for i in range(len(findHighestResults)):
            if findHighestResults[i] is not None:
                self.assertGreaterEqual(testInputs[i].get('budget'), findHighestResults[i].get('price'))
if __name__ == '__main__':
    unittest.main()