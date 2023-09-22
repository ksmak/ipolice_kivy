import json
import asynckivy as ak

from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock

from View.MainScreen.main_screen import MainScreenView
from Utility.helper import get_by_id


class MainScreenController:
    """
    The `MainScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = model  # Model.main_screen.MainScreenModel
        self.view = MainScreenView(controller=self, model=self.model)

    def get_view(self) -> MainScreenView:
        return self.view

    def set_target_screen(self, target_screen: str) -> None:
        self.model.target_screen = target_screen

    def generate_category_items(self, *args) -> None:
        Clock.start_clock()
        req = UrlRequest(self.model.HOST_API + 'categories/')
        while not req.is_finished:  
            Clock.tick()            
        Clock.stop_clock()   
        self.model.category_items = req.result

    def generate_items(self, *args) -> None:
        Clock.start_clock()
        req = UrlRequest(self.model.HOST_API + 'items/')
        while not req.is_finished:  
            Clock.tick()            
        Clock.stop_clock()   
        items = req.result
        # append additional fields
        for item in items:
            item['id'] = str(item['id'])
            item['image_count'] = self.model.ITEM_IMAGE_COUNT
            item['is_favorite'] = False
            item['controller'] = self
            s = [item['title'], item['text']]
            item['fulltext'] = ('#').join(s).lower()
        
        self.model.items = items      

    def generate_fav_items(self, *args) -> None:
        f_items = []
        self.model.fav_items = []
        path_to_fav_items = self.model.DATA_DIR.joinpath(
            self.model.DATA_DIR, "fav_items.json"
        )
        if path_to_fav_items.exists():
            with open(path_to_fav_items) as json_file:
                f_items = json.loads(json_file.read())
        fav_items = []
        for item in self.model.items:
            if item['id'] in f_items:
                item['is_favorite'] = True
                fav_items.append(item)
        self.model.fav_items = fav_items

    def generate_last_items(self, *args) -> None:
        last_items = []
        last_items_count = min(
            self.model.LAST_ITEMS_COUNT, len(self.model.items))
        for i in range(last_items_count):
            last_items.append(self.model.items[i])
        self.model.last_items = last_items

    def generate_message_items(self, *args) -> None:
        messages = []
        path_to_message_items = self.model.DATA_DIR.joinpath(
            self.model.DATA_DIR, "message_items.json"
        )
        if path_to_message_items.exists():
            with open(path_to_message_items) as json_file:
                messages = json.loads(json_file.read())
        for msg in messages:
            msg['id'] = str(msg['id'])
            msg['is_own'] = msg['from_id'] == self.model.user_id
            msg['is_read'] = not msg['date_of_read']
            msg['is_send'] = not msg['date_of_send']
            msg['controller'] = self
        self.model.message_items = messages

    def set_browse_type(self, browse_type: str, *args) -> None:
        self.model.browse_type = browse_type

    def search_by_category(self, category: int) -> None:
        async def search() -> None:
            find_items = []
            for item in self.model.items:
                if (item['category'] == category):
                    find_items.append(item)
                await ak.sleep(0)
            self.model.find_items = find_items
            self.model.is_loading = False
            self.model.notify_observers()

        self.model.is_first_open = False
        self.model.is_loading = True
        self.model.find_items = []

        ak.start(search())

    def open_search(self):
        self.model.find_items = []
        self.model.is_first_open = True

    def set_favorite_item(self, id: int) -> None:
        res = [d for d in self.model.items if d['id'] == id]
        if res:
            res[0]['is_favorite'] = not res[0]['is_favorite']
            if res[0] not in self.model.fav_items and res[0]['is_favorite']:
                self.model.fav_items.append(res[0])
            else:
                self.model.fav_items.remove(res[0])

    def set_current_item(self, id: int) -> None:
        res = [d for d in self.model.items if d['id'] == id]
        if res:
            self.model.current_item = res[0]

    def remove_message(self, id: int, *args) -> None:
        res = [d for d in self.model.message_items if d['id'] == id]
        if res:
            self.model.message_items.remove(res[0])
            self.model.notify_observers()

    def remove_all_messages(self, *args) -> None:
        self.model.message_items = []
        self.model.notify_observers()
