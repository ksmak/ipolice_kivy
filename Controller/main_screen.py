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
