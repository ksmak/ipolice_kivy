from Utility.helper import get_by_id
from Model.base_model import BaseScreenModel
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR.joinpath("assets", "data")


class MainModel(BaseScreenModel):
    """
    Implements the logic of the
    :class:`~View.main_screen.MainScreen.MainScreenView` class.
    """

    def __init__(self):
        # constants
        self.ITEM_IMAGE_COUNT = 5
        self.LAST_ITEMS_COUNT = 10
        # loading categories
        self._category_description = []
        path_to_category_description = DATA_DIR.joinpath(
            DATA_DIR, "category_description.json"
        )
        if path_to_category_description.exists():
            with open(path_to_category_description) as json_file:
                self._category_description = json.loads(json_file.read())
        # loading items
        self._items_description = []
        path_to_items_description = DATA_DIR.joinpath(
            DATA_DIR, "items_description.json"
        )
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
        last_items_count = self.LAST_ITEMS_COUNT
        if len(self._items_description) < self.LAST_ITEMS_COUNT:
            last_items_count = len(self._items_description)
        for i in range(last_items_count):
            self._last_items.append(self._items_description[i])

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
