from functools import partial

from View.base_screen import BaseScreenView
from .components.list.history_item import HistoryItem
from View.MainScreen.components.recycleview.gallery_label import GalleryLabel  # noqa
from View.MainScreen.components.recycleview.list_label import ListLabel  # noqa
from View.MainScreen.components.recycleview.grid_label import GridLabel  # noqa
from View.MainScreen.components.recycleview.rv_box_layout import BoxRecycleLayout  # noqa
from View.MainScreen.components.recycleview.rv_grid_layout import GridRecycleLayout  # noqa


class SearchScreenView(BaseScreenView):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.controller.generate_history_items()
        
    def on_pre_enter(self):
        self.create_history_items()
        self.controller.set_target_screen('search screen')
        self.refresh_layouts()

    def create_history_items(self):
        self.ids.history_container.clear_widgets()
        for history_item in self.model.history_items:
            item = HistoryItem(
                title=history_item['title']
            )
            callback_function = partial(
                self.history_search, history_item['title'])
            item.bind(on_press=callback_function)
            callback_function = partial(
                self.remove_history_item, history_item)
            item.ids.history_icon.bind(on_press=callback_function)
            self.ids.history_container.add_widget(item)

    def remove_history_item(self, item: dict, *args) -> None:
        self.controller.remove_history_item(item)

    def remove_all_history_items(self):
        self.controller.remove_all_history_items()

    def history_search(self, sf: str, *args):
        self.ids.search_field.text = sf
        self.controller.search(sf.lower())

    def search(self):
        self.controller.search(self.ids.search_field.text.lower())
    
    def refresh_layouts(self):
        print(f'is_first_open={self.model.is_first_open}')
        print(f'is_loading={self.model.is_loading}')
        print(f'history_items={self.model.history_items}')
        print(f'find_items={self.model.find_items}')
        if not self.model.is_first_open \
                or not self.model.history_items:
            self.ids.history_layout.opacity = 0
            self.ids.history_container.opacity = 0
        else:
            self.ids.history_layout.opacity = 1
            self.ids.history_container.opacity = 1
            self.create_history_items()

        if not self.model.is_first_open \
                and not self.model.is_loading:
            self.ids.result_layout.opacity = 1
        else:
            self.ids.result_layout.opacity = 0

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
        self.refresh_layouts()