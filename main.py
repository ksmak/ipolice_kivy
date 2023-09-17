"""
The entry point to the application.

The application uses the MVC template. Adhering to the principles of clean
architecture means ensuring that your application is easy to test, maintain,
and modernize.

You can read more about this template at the links below:

https://github.com/HeaTTheatR/LoginAppMVC
https://en.wikipedia.org/wiki/Model–view–controller
"""

from kivy.core.text import LabelBase

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.font_definitions import theme_font_styles

from View.screens import screens, main_model


class ipolice_kivy(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(self.directory)
        # This is the screen manager that will contain all the screens of your
        # application.
        self.manager_screens = MDScreenManager()

    def build(self) -> MDScreenManager:
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "800"
        self.theme_cls.primary_light_hue = "50"
        self.theme_cls.accent_palette = 'DeepOrange'
        self.theme_cls.accent_hue = "800"
        # LabelBase.register(
        #     name="NotoSans",
        #     fn_regular="assets/fonts/NotoSans-Regular.ttf"
        # )
        # theme_font_styles.append('NotoSans')
        # self.theme_cls.font_styles["NotoSans"] = [
        #     "NotoSans",
        #     16,
        #     False,
        #     0.15,
        # ]
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


ipolice_kivy().run()
