import json

from kivy.logger import Logger

from Model.base_model import BaseScreenModel
from Utility.helper import get_by_id


class MainModel(BaseScreenModel):
    """
    Implements the logic of the
    :class:`~View.main_screen.MainScreen.MainScreenView` class.
    """

    def __init__(self, DATA_DIR, LAST_ITEMS_COUNT):
        # loading categories
        self._category_description = []
        path_to_category_description = DATA_DIR.joinpath(
            DATA_DIR, "category_description.json"
        )
        Logger.info('python. path for category: %s', path_to_category_description)
        if path_to_category_description.exists():
            with open(path_to_category_description) as json_file:
                self._category_description = json.loads(json_file.read())
        # loading items
        self._items_description = []
        path_to_items_description = DATA_DIR.joinpath(
            DATA_DIR, "items_description.json"
        )
        Logger.info('python. path for items: %s', path_to_items_description)
        if path_to_items_description.exists():
            with open(path_to_items_description) as json_file:
                self._items_description = json.loads(json_file.read())
        # generate fulltext
        for item in self._items_description:
            s = [item['title'], item['text']]
            category = get_by_id(item['category'], self._category_description)
            for field in category['fields']:
                s.append(item[field])
            item['fulltext'] = ('#').join(s).lower()
        # load search_history
        self._search_history_description = []
        path_to_search_history_description = DATA_DIR.joinpath(
            DATA_DIR, "search_history_description.json"
        )
        Logger.info('python. path for history items: %s', path_to_search_history_description)
        if path_to_search_history_description.exists():
            with open(path_to_search_history_description) as json_file:
                self._search_history_description = json.loads(json_file.read())
        # set search_loading
        self._search_loading = False
        # set find items
        self._find_items = []
        # set first search detect
        self._is_first_search = False
        # browse type (gallery, list, grid)
        self._browse_type = 'gallery'
        # set last items list
        self._last_items = []
        last_items_count = LAST_ITEMS_COUNT
        if len(self._items_description) < LAST_ITEMS_COUNT:
            last_items_count = len(self._items_description)
        for i in range(last_items_count):
            self._last_items.append(self._items_description[i])
        # load favorite items
        self._favorite_items_description = []
        path_to_favorite_items_description = DATA_DIR.joinpath(
            DATA_DIR, "favorite_items_description.json"
        )
        Logger.info('python. path for favorite items: %s', path_to_favorite_items_description)
        if path_to_favorite_items_description.exists():
            with open(path_to_favorite_items_description) as json_file:
                self._favorite_items_description = json.loads(json_file.read())
        # set tab name
        self._tab_name = 'main'
        # set current item
        self._current_item = None
        # set target screen
        self.target_screen = 'main screen'
        # load text messages
        self._messages = []
        path_to_messages = DATA_DIR.joinpath(
            DATA_DIR, "messages.json"
        )
        Logger.info('python. path for messages: %s', path_to_messages)
        if path_to_messages.exists():
            with open(path_to_messages) as json_file:
                self._messages = json.loads(json_file.read())
        # set user_id
        self.user_id = 15
        # set current message
        self._current_message = {}

        self._observers = []

    @property
    def category_description(self):
        return self._category_description

    @property
    def items_description(self):
        return self._items_description

    @property
    def search_history_description(self):
        return self._search_history_description

    @property
    def search_loading(self):
        return self._search_loading

    @property
    def find_items(self):
        return self._find_items

    @property
    def is_first_search(self):
        return self._is_first_search

    @property
    def browse_type(self):
        return self._browse_type

    @property
    def last_items(self):
        return self._last_items

    @property
    def favorite_items(self):
        return self._favorite_items_description

    @property
    def tab_name(self):
        return self._tab_name

    @property
    def current_item(self):
        return self._current_item

    @property
    def messages(self):
        return self._messages

    @property
    def current_message(self):
        return self._current_message


    @category_description.setter
    def category_description(self, value):
        self._category_description = value
        self.notify_observers()

    @items_description.setter
    def items_description(self, value):
        self._category_description = value
        self.notify_observers()

    @search_history_description.setter
    def search_history_description(self, value):
        self._search_history_description = value
        self.notify_observers()

    @search_loading.setter
    def search_loading(self, value):
        self._search_loading = value
        self.notify_observers()

    @find_items.setter
    def find_items(self, value):
        self._find_items = value
        self.notify_observers()

    @is_first_search.setter
    def is_first_search(self, value):
        self._is_first_search = value
        self.notify_observers()

    @browse_type.setter
    def browse_type(self, value):
        self._browse_type = value
        self.notify_observers()

    @last_items.setter
    def last_items(self, value):
        self._last_items = value
        self.notify_observers()

    @favorite_items.setter
    def favorite_items(self, value):
        self._favorite_items_description = value
        self.notify_observers()

    @tab_name.setter
    def tab_name(self, value):
        self._tab_name = value
        self.notify_observers()

    @current_item.setter
    def current_item(self, value):
        self._current_item = value
        # self.notify_observers()
    
    @messages.setter
    def messages(self, value):
        self._messages = value
        self.notify_observers()
    
    @current_message.setter
    def current_message(self, value):
        self._current_message = value
        self.notify_observers()
