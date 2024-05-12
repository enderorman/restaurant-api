from menu_service import MenuService
from file_service import FileService
fileService = FileService()
menuService = MenuService(fileService)
