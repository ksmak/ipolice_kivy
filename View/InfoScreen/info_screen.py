from View.base_screen import BaseScreenView
from Utility.helper import format_date


class InfoScreenView(BaseScreenView):
    def on_pre_enter(self) -> None:
        self.app.screen_stack.append('info screen')

        self.ids.photo.source = self.model.current_info['photo1']
        self.ids.title.text = self.model.current_info['title']
        self.ids.text.text = self.model.current_info['text']
        self.ids.date_add.text = self.model.current_info['date_add']

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
