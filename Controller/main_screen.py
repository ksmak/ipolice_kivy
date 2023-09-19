import asynckivy as ak

from View.MainScreen.main_screen import MainScreenView


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

    def set_browse_type(self, browse_type: str, *args) -> None:
        self.model.browse_type = browse_type

    def search_by_category(self, category: int) -> None:

        async def search(categroy: int) -> None:
            find_items = []
            for item in self.model.items_description:
                if (item['category'] == category):
                    find_items.append(item)
                await ak.sleep(0)
            self.model.find_items = find_items
            self.model.search_loading = False

        self.model.is_first_search = True
        self.model.search_loading = True
        self.model.find_items = []

        ak.start(search(category))

    def open_search(self):
        self.model.is_first_search = False
        self.model.find_items = []
    
    def set_favorite_item(self, id: int) -> None:
        for item in self.model.items_description:
            if item['id'] == id:
                self.model.favorite_items.append(item)
                break
    
    def unset_favorite_item(self, id: int) -> None:
        for item in self.model.favorite_items:
            if item['id'] == id:
                self.model.favorite_items.remove(item)
                break
    
    def set_tab_name(self, tab_name: str) -> None:
        self.model.tab_name = tab_name
    
    def set_current_item(self, id: int) -> None:
        for item in self.model.items_description:
            if item['id'] == id:
                self.model.current_item = item
                break
    
    def remove_message(self, id: int, *args) -> None:
        for msg in self.model.messages:
            if msg['id'] == id:
                self.model.messages.remove(msg)
                self.model.notify_observers()
                break
    
    def remove_all_messages(self, *args) -> None:
        self.model.messages = []
