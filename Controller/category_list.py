import asynckivy as ak

from View.CategoryListScreen.category_list import CategoryListScreenView


class CategoryListScreenController:
    """
    Category list screen controller.
    """

    def __init__(self, model):
        self.model = model
        self.view = CategoryListScreenView(controller=self, model=self.model)

    def get_view(self) -> CategoryListScreenView:
        return self.view

    def set_target_screen(self, target_screen: str) -> None:
        self.model.target_screen = target_screen

    def search_by_category(self, id: int) -> None:
        async def search() -> None:
            find_items = []
            for item in self.model.items:
                if (item['category'] == id):
                    find_items.append(item)
                await ak.sleep(0)
            self.model.find_items = find_items
            self.model.is_loading = False
            self.model.notify_observers()

        self.model.is_first_open = False
        self.model.is_loading = True
        self.model.find_items = []

        ak.start(search())

    def set_current_category(self, id: int) -> None:
        res = [d for d in self.model.category_items if d['id'] == id]
        if res:
            self.model.current_category = res[0]
