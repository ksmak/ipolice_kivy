# The screens dictionary contains the objects of the models and controllers
# of the screens of the application.


from Model.main_model import MainModel
from Controller.main_screen import MainScreenController
from Controller.search_screen import SearchScreenController
from Controller.item_screen import ItemScreenController
from Controller.info_screen import InfoScreenController
from Controller.category_list import CategoryListScreenController

main_model = MainModel

screens = {
    "main screen": {
        "controller": MainScreenController,
    },
    "search screen": {
        "controller": SearchScreenController,
    },
    "item screen": {
        "controller": ItemScreenController,
    },
    "info screen": {
        "controller": InfoScreenController,
    },
    "category list screen": {
        "controller": CategoryListScreenController
    }
}
