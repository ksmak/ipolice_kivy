from View.base_screen import BaseScreenView


class MessageScreenView(BaseScreenView):
    def on_pre_enter(self):
        self.app.target_screen = self.model.target_screen
        self.ids.message_field.focus = True
        self.ids.message_field.helper_text = ''

    def save_message(self, *args):
        msg = self.ids.message_field.text
        
        if len(msg) == 0:
            self.ids.message_field.helper_text = 'Сообщение не должно быть пустым'
            self.ids.message_field.focus = True
            return
        
        data = self.model.current_message
        data['text'] = msg
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