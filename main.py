"""
The entry point to the application.

The application uses the MVC template. Adhering to the principles of clean
architecture means ensuring that your application is easy to test, maintain,
and modernize.

You can read more about this template at the links below:

https://github.com/HeaTTheatR/LoginAppMVC
https://en.wikipedia.org/wiki/Model–view–controller
"""
import asynckivy as ak

from kivy.loader import Loader
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.uix.popup import Popup

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from View.screens import screens, main_model


Loader.num_workers = 4
# Loader.loading_image = Image('loading.gif')

colors = {
    "Teal": {
        "200": "#FFFFFF",
        "500": "#008B8B",
        "700": "#008B8B",
        "A700": "#008B8B",
    },
    "Red": {
        "200": "##003329",
        "500": "##003329",
        "700": "##003329",
        "A700": "##003329",

    },
    "Light": {
        "StatusBar": "E0E0E0",
        "AppBar": "#f2f2f2",
        "Background": "#ffffff",
        "CardsDialogs": "#FFFFFF",
        "FlatButtonDown": "#CCCCCC",
    },
}


class ExitPopup(Popup):
    def __init__(self, **kwargs):
        super(ExitPopup, self).__init__(**kwargs)

    def confirm(self):
        app = MDApp.get_running_app()
        app.close_app()


class ErrorPopup(Popup):
    def __init__(self, **kwargs):
        super(ErrorPopup, self).__init__(**kwargs)
    
    def confirm(self):
        app = MDApp.get_running_app()
        app.close_app()


class ipolice_kivy(MDApp):
    dialog = None
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # load kv
        self.load_all_kv_files(self.directory)
        # This is the screen manager that will contain all the screens of your
        # application.
        self.manager_screens = MDScreenManager()
        self.target_screen = ''
        # self.is_finished_loading_data = False
        Window.bind(on_keyboard=self.on_keyboard)

    def build(self) -> MDScreenManager:
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.colors = colors
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Red"
        self.generate_application_screens()
        return self.manager_screens

    def generate_application_screens(self) -> None:
        """
        Creating and adding screens to the screen manager.
        You should not change this cycle unnecessarily. He is self-sufficient.

        If you need to add any screen, open the `View.screens.py` module and
        see how new screens are added according to the given application
        architecture.
        """

        self.model = main_model()

        for i, name_screen in enumerate(screens.keys()):
            # model = screens[name_screen]["model"]()
            controller = screens[name_screen]["controller"](self.model)
            view = controller.get_view()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)
    
    def close_app(self, *largs):
        super(ipolice_kivy, self).stop(*largs)

    def on_keyboard(self, window, key, *largs):
        if key == 27:
            Logger.info('python. Escape key pressed...')
            if self.target_screen:
                self.manager_screens.current = self.target_screen
                return True

            popup = ExitPopup(separator_height=0, title="Закрыть приложение?",
                              size=(500, 300), size_hint=(None, None))
            popup.open()
            return True

ipolice_kivy().run()
