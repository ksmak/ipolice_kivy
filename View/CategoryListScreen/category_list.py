from functools import partial

from kivymd.uix.list import OneLineAvatarListItem, ImageLeftWidget

from View.base_screen import BaseScreenView


class CategoryListScreenView(BaseScreenView):
    def on_pre_enter(self) -> None:
        self.app.screen_stack.append('category list screen')
        self.generate_category_list()

    def generate_category_list(self) -> None:
        self.ids.category_container.clear_widgets()
        for category in self.model.category_items:
            widget = OneLineAvatarListItem(
                ImageLeftWidget(
                    source=category['photo'],
                    size_hint=(.7, .7)
                ),
                text=category['title'],
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
