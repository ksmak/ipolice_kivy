from pathlib import Path

# from kivy.logger import Logger
from kivy.event import EventDispatcher
from kivy.properties import (
    NumericProperty,
    StringProperty,
    BooleanProperty,
    ListProperty,
    ObjectProperty,
)

from Model.base_model import BaseScreenModel


class MainModel(BaseScreenModel, EventDispatcher):
    """
    Implements the logic of the
    :class:`~View.main_screen.MainScreen.MainScreenView` class.
    """
    # constants
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR.joinpath("assets", "data")
    ITEM_IMAGE_COUNT = 5
    LAST_ITEMS_COUNT = 10
    HOST_API = 'https://ipolice-production.up.railway.app/api/'
    # properties
    category_items = ListProperty()
    items = ListProperty()
    last_items = ListProperty()
    fav_items = ListProperty()
    find_items = ListProperty()
    message_items = ListProperty()
    history_items = ListProperty()
    user_id = NumericProperty(15)
    is_loading = BooleanProperty(False)
    target_screen = StringProperty()
    is_first_open = BooleanProperty()
    browse_type = StringProperty('gallery')
    current_item = ObjectProperty()
    current_message = ObjectProperty()
    search_field = StringProperty()

    def __init__(self):
        pass

        # # set search_loading
        # self._search_loading = False
        # # set find items
        # self._find_items = []
        # # set first search detect
        # self._is_first_search = False
        # # browse type (gallery, list, grid)
        # self._browse_type = 'gallery'

        # # load favorite items
        # self._favorite_items_description = []
        # path_to_favorite_items_description = DATA_DIR.joinpath(
        #     DATA_DIR, "favorite_items_description.json"
        # )
        # Logger.info('python. path for favorite items: %s',
        #             path_to_favorite_items_description)
        # if path_to_favorite_items_description.exists():
        #     with open(path_to_favorite_items_description) as json_file:
        #       self._favorite_items_description = json.loads(json_file.read())
        # # set tab name
        # self._tab_name = 'main'
        # # set current item
        # self._current_item = None
        # # set target screen
        # self.target_screen = 'main screen'

        # # set user_id
        # self.user_id = 15
        # # set current message
        # self._current_message = {}

        self._observers = []
