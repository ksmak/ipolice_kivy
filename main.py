"""
The entry point to the application.

The application uses the MVC template. Adhering to the principles of clean
architecture means ensuring that your application is easy to test, maintain,
and modernize.

You can read more about this template at the links below:

https://github.com/HeaTTheatR/LoginAppMVC
https://en.wikipedia.org/wiki/Model–view–controller
"""
from kivy.loader import Loader
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.uix.popup import Popup

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from View.screens import screens, main_model


Loader.num_workers = 4
# Loader.loading_image = Image('loading.gif')


class ExitPopup(Popup):
    def __init__(self, **kwargs):
        super(ExitPopup, self).__init__(**kwargs)

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
        Window.bind(on_keyboard=self.on_keyboard)

    def build(self) -> MDScreenManager:
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "800"
        self.theme_cls.primary_light_hue = "50"
        self.theme_cls.accent_palette = 'DeepOrange'
        self.theme_cls.accent_hue = "900"
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

        model = main_model()

        for i, name_screen in enumerate(screens.keys()):
            # model = screens[name_screen]["model"]()
            controller = screens[name_screen]["controller"](model)
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

            popup = ExitPopup(title="Закрыть приложение?",
                              size=(400, 300), size_hint=(None, None))
            popup.open()
            return True

ipolice_kivy().run()
