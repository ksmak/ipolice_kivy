from View.ItemScreen.item_screen import ItemScreenView


class ItemScreenController:
    """
    Item screen controller.
    """

    def __init__(self, model):
        self.model = model
        self.view = ItemScreenView(controller=self, model=self.model)

    def get_view(self) -> ItemScreenView:
        return self.view

    def set_favorite_item(self, id: int) -> None:
        res = [d for d in self.model.items if d['id'] == id]
        if res:
            res[0]['is_favorite'] = not res[0]['is_favorite']
            if res[0] not in self.model.fav_items and res[0]['is_favorite']:
                self.model.fav_items.append(res[0])
            else:
                self.model.fav_items.remove(res[0])
