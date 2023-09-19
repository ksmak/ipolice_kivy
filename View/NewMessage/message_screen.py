from View.base_screen import BaseScreenView
import datetime

class MessageScreenView(BaseScreenView):
    def save_message(self, *args):
        data = self.model.current_message
        data['text'] = self.ids.message_field.text
        data['date_of_creation'] = datetime.datetime.now().strftime('D.M.Y H:m:s')
        self.controller.save_message(data)
        self.manager_screens.current = self.model.target_screen
    
    def close_screen(self, *args):
        self.manager_screens.current = self.model.target_screen

    def model_is_changed(self) -> None:
            """
            Called whenever any change has occurred in the data model.
            The view in this method tracks these changes and updates the UI
            according to these changes.
            """