from View.NewMessage.message_screen import MessageScreenView


class MessageScreenController:
    """
    The `MainScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = model  # Model.main_screen.MainScreenModel
        self.view = MessageScreenView(controller=self, model=self.model)

    def get_view(self) -> MessageScreenView:
        return self.view
    
    def save_message(self, data, *args) -> None:
        self.model.current_message = data
        self.model.messages.append(data)