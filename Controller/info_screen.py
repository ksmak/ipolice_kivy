from View.InfoScreen.info_screen import InfoScreenView


class InfoScreenController:
    """
    Info screen controller.
    """

    def __init__(self, model):
        self.model = model
        self.view = InfoScreenView(controller=self, model=self.model)

    def get_view(self) -> InfoScreenView:
        return self.view
