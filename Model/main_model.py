from pathlib import Path

from kivy.event import EventDispatcher
from kivy.properties import (
    StringProperty,
    BooleanProperty,
    ListProperty,
    ObjectProperty,
    DictProperty,
)

from Model.base_model import BaseScreenModel


class MainModel(BaseScreenModel, EventDispatcher):
    """
    Main model
    """
    # constants
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR.joinpath("assets", "data")
    IMAGE_DIR = BASE_DIR.joinpath("assets", "images")
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
    is_loading = BooleanProperty(False)
    is_first_open = BooleanProperty()
    current_item = ObjectProperty()
    current_message = ObjectProperty()
    search_field = StringProperty()
    browse_type = StringProperty()
    is_finished = BooleanProperty(False)
    current_category = DictProperty()
    info_items = ListProperty()
    current_info = DictProperty()
    category_result = BooleanProperty(False)
    items_result = BooleanProperty(False)
    info_result = BooleanProperty(False)

    def __init__(self):
        self.user = {}
        self._observers = []
