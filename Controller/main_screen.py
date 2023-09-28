import json
import asynckivy as ak

from kivy.network.urlrequest import UrlRequest

from View.MainScreen.main_screen import MainScreenView
from Utility.helper import save_file


class MainScreenController:
    """
    The `MainScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = model
        self.view = MainScreenView(controller=self, model=self.model)

    def get_view(self) -> MainScreenView:
        return self.view

    def generate_category_items(self, *args) -> None:
        req = UrlRequest(self.model.HOST_API + 'categories/')
        req.wait()
        self.model.category_items = req.result

    def generate_items(self, *args) -> None:
        req = UrlRequest(self.model.HOST_API + 'items/')
        req.wait()
        items = req.result
        # append additional fields
        for item in items:
            item['id'] = str(item['id'])
            item['image_count'] = self.model.ITEM_IMAGE_COUNT
            item['is_favorite'] = False
            item['controller'] = self
            # fulltext search field
            s = [item['title'].lower(), item['text'].lower()]
            item['fulltext'] = ('#').join(s)
            item['controller'] = self
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
            if any(item['id'] == f['id'] for f in f_items):
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
    
    def set_user_settings(self, *args) -> None:
        path_to_settings = self.model.DATA_DIR.joinpath(
            self.model.DATA_DIR, "user_settings.json"
        )
        if path_to_settings.exists():
            with open(path_to_settings) as json_file:
                self.model.user = json.loads(json_file.read())
        self.model.browse_type = self.model.user['browse_type']
    
    def load_data(self) -> None:
        async def start_load():
            ak.sleep(0)
            self.generate_category_items()
            self.generate_items()
            self.generate_fav_items()
            self.generate_last_items()
            self.set_user_settings()
            self.model.notify_observers()
            
        ak.start(start_load())
    
    def set_target_screen(self, target_screen: str) -> None:
        self.model.target_screen = target_screen

    def set_browse_type(self, browse_type: str, *args) -> None:
        self.model.browse_type = browse_type
        self.model.user['browse_type'] = browse_type
        save_file(self.model.DATA_DIR, 'user_settings.json', self.model.user)

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

            fav_items = []
            for item in self.model.fav_items:
                fav_items.append({'id': item['id']})
            
            save_file(self.model.DATA_DIR, "fav_items.json", fav_items)    

    def set_current_item(self, id: int) -> None:
        res = [d for d in self.model.items if d['id'] == id]
        if res:
            self.model.current_item = res[0]
    
    def set_current_category(self, id: int) -> None:
        res = [d for d in self.model.category_items if d['id'] == id]
        if res:
            self.model.current_category = res[0]
