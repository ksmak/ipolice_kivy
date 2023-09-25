# The screens dictionary contains the objects of the models and controllers
# of the screens of the application.


from Model.main_model import MainModel
from Controller.main_screen import MainScreenController
from Controller.search_screen import SearchScreenController
from Controller.item_screen import ItemScreenController

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
}
