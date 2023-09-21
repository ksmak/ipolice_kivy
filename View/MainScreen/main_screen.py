from functools import partial

from View.base_screen import BaseScreenView
from .components.card.category_card import CategoryCard
from .components.recycleview.gallery_label import GalleryLabel  # noqa
from .components.recycleview.list_label import ListLabel  # noqa
from .components.recycleview.grid_label import GridLabel  # noqa
from .components.recycleview.rv_box_layout import BoxRecycleLayout  # noqa
from .components.recycleview.rv_grid_layout import GridRecycleLayout  # noqa
from .components.recycleview.message_label import MessageLabel  # noqa


class MainScreenView(BaseScreenView):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.controller.generate_category_items()
        self.controller.generate_items()
        self.controller.generate_fav_items()
        self.controller.generate_last_items()
        self.controller.generate_message_items()
        self.generate_category_cards()

    def on_pre_enter(self) -> None:
        if self.model.browse_type == 'gallery':
            self.ids.gallery_rv.refresh_from_data()
        elif self.model.browse_type == 'list':
            self.ids.list_rv.refresh_from_data()
        elif self.model.browse_type == 'grid':
            self.ids.grid_rv.refresh_from_data()
        self.controller.set_target_screen('main screen')

    def generate_category_cards(self) -> None:
        self.ids.category_list_container.clear_widgets()
        for category in self.model.category_items:
            card = CategoryCard(
                category_icon=str(self.model.BASE_DIR) +
                '/' + category['icon'],
                category_name=category['name']
            )
            callback_function = partial(
                self.open_category_items, category['id'])
            card.ids.card_button.bind(on_release=callback_function)
            self.ids.category_list_container.add_widget(card)

    def open_category_items(self, category: int, *args) -> None:
        self.controller.search_by_category(category)
        self.manager_screens.current = 'search screen'

    def to_search_screen(self) -> None:
        self.controller.open_search()
        self.manager_screens.current = 'search screen'

    def remove_all_messages(self, *args) -> None:
        self.controller.remove_all_messages()

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
