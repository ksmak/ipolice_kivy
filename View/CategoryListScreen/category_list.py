from functools import partial

from kivymd.uix.list import OneLineAvatarListItem, ImageLeftWidget

from View.base_screen import BaseScreenView
from .components.list.category_item import CategoryItem


class CategoryListScreenView(BaseScreenView):
    def on_pre_enter(self) -> None:
        self.app.screen_stack.append('category list screen')
        self.generate_category_list()

    def calc_count_items(self) -> dict:
        cnts = {}
        for item in self.model.items:
            category = 'id_' + str(item['category'])
            if category in cnts:
                cnts[category] = cnts[category] + 1
            else:
                cnts[category] = 1

        return cnts

    def generate_category_list(self) -> None:
        cnts = self.calc_count_items()
        self.ids.category_container.clear_widgets()
        for category in self.model.category_items:
            cnt_text = 'Количество: ' + \
                str(cnts.get('id_' + str(category['id']), 0))
            widget = CategoryItem(
                photo=category['photo'],
                title=category['title'],
                text=cnt_text
            )
            callable_function = partial(
                self.open_category_item, category['id'])
            widget.bind(on_release=callable_function)
            self.ids.category_container.add_widget(widget)

    def open_category_item(self, category_id: int, *args) -> None:
        self.controller.set_current_category(category_id)
        self.controller.search_by_category(category_id)
        self.manager_screens.current = 'search screen'

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
