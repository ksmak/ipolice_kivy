import asynckivy as ak

from View.SearchScreen.search_screen import SearchScreenView


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

    def remove_search_history_item(self, item):
        if item in self.model.search_history_description:
            self.model.search_history_description.remove(item)
            self.model.notify_observers()

    def remove_all_search_history_items(self):
        self.model.search_history_description = []

    def search(self, sf: str, *args):

        async def search_process(st: str):
            find_items = []
            for item in self.model.items_description:
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
                for history in self.model.search_history_description:
                    if history['title'].lower() == sf.lower():
                        break
                else:
                    self.model.search_history_description.append(
                        {
                            "title": sf
                        }
                    )

            self.model.search_loading = False

        self.model.is_first_search = True
        self.model.search_loading = True
        self.model.find_items = []

        ak.start(async_search(sf))

    def set_is_first_search(self, value: bool) -> None:
        self.model.isFirstSearch = value

    def set_browse_type(self, browse_type: str, *args) -> None:
        self.model.browse_type = browse_type
