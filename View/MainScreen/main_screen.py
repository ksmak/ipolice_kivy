from functools import partial

from View.base_screen import BaseScreenView
from .components.card.category_card import CategoryCard
from .components.layout.result_header import ResultHeader
from .components.recycleview.gallery_label import GalleryLabel  # noqa
from .components.recycleview.list_label import ListLabel  # noqa
from .components.recycleview.grid_label import GridLabel  # noqa
from .components.recycleview.rv_box_layout import BoxRecycleLayout  # noqa
from .components.recycleview.rv_grid_layout import GridRecycleLayout  # noqa
from .components.textfield.search import SearchField  # noqa


class MainScreenView(BaseScreenView):

    def on_enter(self):
        self.ids.category_list_container.clear_widgets()
        self.generate_category_cards()
        self.refresh_recycleview()
        self.result_header = ResultHeader(
            title='Последние добавления',
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

        self.ids.result_header.clear_widgets()
        self.ids.result_header.add_widget(self.result_header)
        self.refresh_result_header()

    def generate_category_cards(self):
        for category in self.model.category_description:
            card = CategoryCard(
                category_icon=category['icon'],
                category_name=category['name']
            )
            callback_function = partial(
                self.open_category_items, category['id'])
            card.ids.card_button.bind(on_release=callback_function)
            self.ids.category_list_container.add_widget(card)

    def open_category_items(self, category: int, *args) -> None:
        self.controller.search_by_category(category)
        self.manager_screens.current = 'search screen'

    def to_search_screen(self):
        self.controller.open_search()
        self.manager_screens.current = 'search screen'

    def refresh_recycleview(self):
        data = []
        for item in self.model.last_items:
            data.append({
                'title': item['title'],
                'text': item['text'],
                'date': item['date_of_creation'],
                'photo1': item['photo1'],
                'photo2': item['photo2'],
                'photo3': item['photo3'],
                'photo4': item['photo4'],
                'photo5': item['photo5'],
                'image_count': self.model.ITEM_IMAGE_COUNT,
            })
        self.ids.gallery_rv.data = data
        self.ids.gallery_rv.refresh_from_data()
        self.ids.list_rv.data = data
        self.ids.list_rv.refresh_from_data()
        self.ids.grid_rv.data = data
        self.ids.grid_rv.refresh_from_data()

    def refresh_result_header(self):
        self.result_header.button = self.model.browse_type

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
        self.refresh_result_header()