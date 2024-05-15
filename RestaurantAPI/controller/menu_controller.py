from service import MenuService
from service import FileService
import json
from urllib.parse import urlparse, parse_qs

class MenuController:
    def __init__(self, file_path):
        self.menuService = MenuService(FileService(file_path))

    def handle_request(self, request):
        if request.command == 'GET':
            self._handle_get_request(request)

        elif request.command == 'POST':
            self._handle_post_request(request)

    def _handle_get_request(self, request):
        parsed_path = urlparse(request.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        if path == '/listMeals':
            is_vegetarian = query_params.get('is_vegetarian', ["false"])[0].lower() == 'true'
            is_vegan = query_params.get('is_vegan', ["false"])[0].lower() == 'true'
            meals = self._listMeals(is_vegetarian, is_vegan)
            return self._send_json_response(request, meals)
        elif path == '/getMeal':
            meal_id = int(query_params.get('id', [None])[0])
            meal = self.menuService._getMealByID(meal_id)
            if meal:
                return self._send_json_response(request, meal)
            else:
                return self._send_error_response(request, 404, b'Meal not found.')
        elif path == '/search':
            text = query_params.get('query', [None])[0]
            if text is not None:
                searchResult = self._search(text)
                if searchResult is not None:
                    return self._send_json_response(request, searchResult)
                else:
                    return self._send_error_response(request, 404, b'Search text not found.')
            else:
                return self._send_error_response(request, 400, b'Search text is required.')


    def _handle_post_request(self, request):
        parsed_path = urlparse(request.path)
        path = parsed_path.path
        content_length = int(request.headers['Content-Length'])
        post_data = request.rfile.read(content_length)
        post_params = parse_qs(post_data.decode())
        if path == '/quality':
            meal_id = post_params.get('meal_id', [None])[0]
            if meal_id is None:
                return self._send_error_response(request, 400, b'Meal ID is required.')
            ingredient_qualities = {param_name: param_value[0] for param_name, param_value in post_params.items() if
                                    param_name != 'meal_id'}
            meal_id = int(meal_id)
            meal = self.menuService._getMealByID(meal_id)
            if meal is not None:
                quality_result = self._calculateQualityScore(meal_id, ingredient_qualities)
                return self._send_json_response(request, quality_result)
            else:
                return self._send_error_response(request, 404, b'Meal not found.')
        elif path == "/price":
            meal_id = post_params.get('meal_id', [None])[0]
            if meal_id is None:
                return self._send_error_response(request, 400, b'Meal ID is required.')
            ingredient_qualities = {param_name: param_value[0] for param_name, param_value in post_params.items() if
                                    param_name != 'meal_id'}
            meal_id = int(meal_id)
            meal = self.menuService._getMealByID(meal_id)
            if meal is not None:
                price_result = self._calculatePrice(meal_id, ingredient_qualities)
                return self._send_json_response(request, price_result)
            else:
                return self._send_error_response(request, 400, b'Meal not found.')
        elif path == '/random':
            budget = int(post_params.get('budget', [None])[0])
            random_meal = self._selectRandomMeal(budget)
            if random_meal:
                return self._send_json_response(request, random_meal)
            else:
                return self._send_error_response(request, 404, b'No meal found within budget.')
        elif path == '/findHighest':
            budget = post_params.get('budget', [None])[0]
            if budget is None:
                return self._send_error_response(request, 400, b'Budget is required.')
            budget = float(budget)
            is_vegetarian = post_params.get('is_vegetarian', ["false"])[0].lower() == 'true'
            is_vegan = post_params.get('is_vegan', ["false"])[0].lower() == 'true'
            highestQualityMeal = self._findHighest(budget, is_vegetarian, is_vegan)
            if highestQualityMeal is not None:
                return self._send_json_response(request, highestQualityMeal)
            else:
                return self._send_error_response(request, 404, b'No meal found within budget.')
        elif path == '/findHighestOfMeal':
            meal_id = post_params.get('meal_id', [None])[0]
            budget = post_params.get('budget', [None])[0]
            if meal_id is None:
                return self._send_error_response(request, 400, b'Meal ID is required.')
            if budget is None:
                return self._send_error_response(request, 400, b'Budget is required.')
            meal_id = int(meal_id)
            budget = float(budget)
            highestQualityOfMeal = self._findHighestOfMeal(meal_id, budget)
            if highestQualityOfMeal is not None:
                return self._send_json_response(request, highestQualityOfMeal)
            else:
                return self._send_error_response(request, 404, b'No meal found within budget')

    def _listMeals(self, is_vegetarian, is_vegan):
        return self.menuService.listMeals(is_vegetarian, is_vegan)

    def _getMeal(self, meal_id):
        return self.menuService.getMeal(meal_id)

    def _calculateQualityScore(self, meal_id, ingredients):
        return self.menuService.calculateQualityScore(meal_id, ingredients)

    def _calculatePrice(self, meal_id, ingredients):
        return self.menuService.calculatePrice(meal_id, ingredients)

    def _selectRandomMeal(self, budget=None):
        return self.menuService.selectRandomMealWithBudget(budget)

    def _search(self, text):
        return self.menuService.search(text)

    def _findHighest(self, budget, is_vegetarian, is_vegan):
        return self.menuService.findHighest(budget, is_vegetarian, is_vegan)

    def _findHighestOfMeal(self, meal_id, budget):
        return self.menuService.findHighestOfMeal(meal_id, budget)

    def _send_json_response(self, request, data):
        request.send_response(200)
        request.send_header('Content-type', 'application/json')
        request.end_headers()
        request.wfile.write(json.dumps(data).encode())

    def _send_error_response(self, request, status_code, message):
        request.send_response(status_code)
        request.send_header('Content-type', 'text/plain')
        request.end_headers()
        request.wfile.write(message)

