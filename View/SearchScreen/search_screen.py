from functools import partial

from kivy.animation import Animation

from kivymd.uix.menu import MDDropdownMenu

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
        self.app.target_screen = 'main screen'
        self.controller.set_target_screen('search screen')
        self.create_history_items()
        self.refresh_layouts()
        self.create_category_menu()

    def create_history_items(self):
        self.ids.history_container.clear_widgets()
        for history_item in self.model.history_items:
            item = HistoryItem(
                title=history_item['title']
            )
            item.opacity = 0
            callback_function = partial(
                self.history_search, history_item['title'])
            item.bind(on_press=callback_function)
            callback_function = partial(
                self.remove_history_item, history_item)
            item.ids.history_icon.bind(on_press=callback_function)
            self.ids.history_container.add_widget(item)
            Animation(opacity=1, duration=.25).start(item)

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
    
    def create_category_menu(self):
        self.menu_items = [
            {
                "text": c['title'],
                "on_release": lambda x=c['title']: self.category_menu_callback(x),
            } for c in self.model.category_items
        ]
        self.category_menu = MDDropdownMenu(
            caller=self.ids.cat_item, 
            items=self.menu_items,
            position="center"
        )
        self.category_menu.bind()
        if self.model.current_category:
            self.ids.cat_item.set_item(self.model.current_category['title'])
        else:
            self.ids.cat_item.set_item('Все')

    def category_menu_callback(self, category_title: str):
        self.category_menu.dismiss()
        self.controller.set_current_category(category_title)
        self.ids.cat_item.set_item(category_title)
        self.controller.search(self.ids.search_field.text.lower())


    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
        self.refresh_layouts()
