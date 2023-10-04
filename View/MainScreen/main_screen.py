from functools import partial
import asynckivy as ak

from kivy.clock import Clock
from kivy.animation import Animation

from View.base_screen import BaseScreenView
from .components.card.category_card import CategoryCard
from .components.card.info_card import InfoCard
from .components.recycleview.gallery_label import GalleryLabel  # noqa
from .components.recycleview.list_label import ListLabel  # noqa
from .components.recycleview.grid_label import GridLabel  # noqa
from .components.recycleview.rv_box_layout import BoxRecycleLayout  # noqa
from .components.recycleview.rv_grid_layout import GridRecycleLayout  # noqa


class MainScreenView(BaseScreenView):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.model.is_loading = True
        ak.start(self.controller.generate_category_items())
        ak.start(self.controller.generate_items())
        ak.start(self.controller.generate_info_items())
        ak.start(self.controller.set_user_settings())
        ak.start(self.controller.generate_history_items())

    def on_pre_enter(self) -> None:
        self.app.screen_stack.append('main screen')

    def generate_info_cards(self) -> None:
        if self.model.info_items and len(self.model.info_items) > 0:
            self.ids.info_container.opacity = 1
            self.ids.info_container.clear_widgets()
            for info in self.model.info_items:
                widget = InfoCard()
                widget.icon = info['photo1']
                widget.title = info['title']
                callback_function = partial(self.open_info_item, info['id'])
                widget.bind(on_touch_up=callback_function)
                self.ids.info_container.add_widget(widget)
        Clock.schedule_interval(self.ids.info_container.load_next, 15)

    def generate_category_cards(self) -> None:
        self.ids.category_list_container.clear_widgets()
        for category in self.model.category_items:
            image_path = category['photo'] if category['photo'] else 'default.png'
            card = CategoryCard(
                category_icon=image_path,
                category_name=category['title']
            )
            callback_function = partial(
                self.open_category_items, category['id'])
            card.ids.card_button.bind(on_touch_up=callback_function)
            self.ids.category_list_container.add_widget(card)

    def open_category_items(self, category: int, card_button, touch) -> None:
        if card_button.collide_point(*touch.pos):
            self.controller.set_current_category(category)
            self.controller.search_by_category(category)
            self.manager_screens.current = 'search screen'

    def to_search_screen(self) -> None:
        self.controller.open_search()
        self.manager_screens.current = 'search screen'

    def remove_all_messages(self, *args) -> None:
        self.controller.remove_all_messages()

    def refresh_data_items(self) -> None:
        if self.model.browse_type == 'gallery':
            self.ids.gallery_rv.refresh_from_data()
        elif self.model.browse_type == 'list':
            self.ids.list_rv.refresh_from_data()
        elif self.model.browse_type == 'grid':
            self.ids.grid_rv.refresh_from_data()

    def open_category_list(self) -> None:
        self.manager_screens.current = 'category list screen'

    def open_info_item(self, info_id: int, card, touch) -> None:
        if card.collide_point(*touch.pos):
            self.controller.set_current_info(info_id)
            self.manager_screens.current = 'info screen'

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
        self.model.is_loading = self.model.category_result and self.model.items_result and self.model.info_result
