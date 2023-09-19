from View.NewMessage.new_message_screen import NewMessageScreenView


class NewMessageScreenController:
    """
    The `MainScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = model  # Model.main_screen.MainScreenModel
        self.view = NewMessageScreenView(controller=self, model=self.model)

    def get_view(self) -> NewMessageScreenView:
        return self.view