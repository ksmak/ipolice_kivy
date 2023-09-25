import json

import asynckivy as ak

from View.SearchScreen.search_screen import SearchScreenView
from Utility.helper import save_file


class SearchScreenController:
    """
    The `MainScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = model  # Model.main_screen.MainScreenModel
        self.view = SearchScreenView(controller=self, model=self.model)

    def get_view(self) -> SearchScreenView:
        return self.view

    def set_target_screen(self, target_screen: str) -> None:
        self.model.target_screen = target_screen

    def generate_history_items(self, *args) -> None:
        history_items = []
        path_to_history_items = self.model.DATA_DIR.joinpath(
            self.model.DATA_DIR, "history_items.json"
        )
        if path_to_history_items.exists():
            with open(path_to_history_items) as json_file:
                history_items = json.loads(json_file.read())
        self.model.history_items = history_items

    def remove_history_item(self, item):
        if item in self.model.history_items:
            self.model.history_items.remove(item)
        save_file(self.model.DATA_DIR, "history_items.json", self.model.history_items)
        self.model.notify_observers()    

    def remove_all_history_items(self):
        self.model.history_items = []
        save_file(self.model.DATA_DIR, "history_items.json", self.model.history_items)
        self.model.notify_observers()

    def search(self, sf: str, *args):
        async def search_process(sf: str):
            find_items = []
            arr = sf.split()
            for item in self.model.items:
                for st in arr:
                    if (item['fulltext'].find(st) > 0):
                        find_items.append(item)
                    await ak.sleep(0)
            self.model.find_items = find_items

        async def async_search(sf: str):
            tasks = await ak.wait_any(
                search_process(sf),
                ak.event(self.view.ids.back_button, 'on_press'),
                ak.event(self.view.ids.search_field, 'on_text_validate')
            )

            if tasks[0].finished and self.model.find_items:
                for history in self.model.history_items:
                    if history['title'].lower() == sf.lower():
                        break
                else:
                    self.model.history_items.append({
                        "title": sf
                    })
                    save_file(self.model.DATA_DIR, "history_items.json", self.model.history_items)
            
            self.model.is_loading = False
            self.model.notify_observers()

        self.model.is_first_open = False
        self.model.is_loading = True
        self.model.find_items = []

        ak.start(async_search(sf))

    def set_browse_type(self, browse_type: str, *args) -> None:
        self.model.browse_type = browse_type

    def set_favorite_item(self, id: int):
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
