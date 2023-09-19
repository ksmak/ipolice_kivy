from functools import partial

from View.base_screen import BaseScreenView
from .components.list.search_history_item import SearchHistoryItem
from View.MainScreen.components.recycleview.gallery_label import GalleryLabel  # noqa
from View.MainScreen.components.recycleview.list_label import ListLabel  # noqa
from View.MainScreen.components.recycleview.grid_label import GridLabel  # noqa
from View.MainScreen.components.recycleview.rv_box_layout import BoxRecycleLayout  # noqa
from View.MainScreen.components.recycleview.rv_grid_layout import GridRecycleLayout  # noqa
from View.MainScreen.components.textfield.search import SearchField  # noqa
from View.MainScreen.components.layout.result_header import ResultHeader


class SearchScreenView(BaseScreenView):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.result_header = ResultHeader(
            title='Найдено: ' + str(len(self.model.find_items)),
            button=self.model.browse_type
        )
        callable_function = partial(
            self.controller.set_browse_type, 'gallery')
        self.result_header.ids.gallery_button.bind(
            on_release=callable_function)
        callable_function = partial(
            self.controller.set_browse_type, 'list')
        self.result_header.ids.list_button.bind(
            on_release=callable_function)
        callable_function = partial(self.controller.set_browse_type, 'grid')
        self.result_header.ids.grid_button.bind(
            on_release=callable_function)
        self.ids.result_header.add_widget(self.result_header)
    
    def do_enter(self):
        self.model.target_screen = 'search screen'
    
    def generate_search_history_items(self):
        self.ids.search_history_container.clear_widgets()
        for history_item in self.model.search_history_description:
            item = SearchHistoryItem(
                title=history_item['title']
            )
            callback_function = partial(
                self.history_search, history_item['title'])
            item.bind(on_press=callback_function)
            callback_function = partial(
                self.remove_search_history_item, history_item)
            item.ids.search_history_icon.bind(on_press=callback_function)
            self.ids.search_history_container.add_widget(item)

    def remove_search_history_item(self, item, instance):
        self.controller.remove_search_history_item(item)

    def remove_all_search_history_items(self):
        self.controller.remove_all_search_history_items()

    def history_search(self, sf: str, *args):
        self.ids.search_field.text = sf
        self.controller.search(sf.lower())

    def search(self):
        self.controller.search(self.ids.search_field.text.lower())

    def refresh_recycleview(self):
        self.app.refresh_recycleview(
            self.ids.gallery_rv, 
            self.ids.list_rv, 
            self.ids.grid_rv, 
            self.model.find_items, 
            self.model.favorite_items, 
            self.controller
        )

    def refresh_result_header(self):
        self.result_header.button = self.model.browse_type
        
        self.result_header.title = 'Найдено: ' + \
            str(len(self.model.find_items))

        if self.model.browse_type == 'gallery':
            self.ids.gallery_rv.opacity = 1
            self.ids.list_rv.opacity = 0
            self.ids.grid_rv.opacity = 0
        elif self.model.browse_type == 'list':
            self.ids.gallery_rv.opacity = 0
            self.ids.list_rv.opacity = 1
            self.ids.grid_rv.opacity = 0
        elif self.model.browse_type == 'grid':
            self.ids.gallery_rv.opacity = 0
            self.ids.list_rv.opacity = 0
            self.ids.grid_rv.opacity = 1

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
        self.ids.loading.active = self.model.search_loading

        if self.model.is_first_search \
                or not self.model.search_history_description:
            self.ids.history_layout.opacity = 0
            self.ids.search_history_container.opacity = 0
        else:
            self.ids.history_layout.opacity = 1
            self.ids.search_history_container.opacity = 1
            self.generate_search_history_items()

        if self.model.is_first_search \
                and not self.model.search_loading:
            self.ids.result_layout.opacity = 1
            self.refresh_recycleview()
            self.refresh_result_header()
        else:
            self.ids.result_layout.opacity = 0
