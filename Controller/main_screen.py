import asynckivy as ak

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
    
    def set_controller_for_items(self, *args) -> None:
        for item in self.model.items:
            item['controller'] = self
    
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
