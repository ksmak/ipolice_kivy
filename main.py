"""
The entry point to the application.

The application uses the MVC template. Adhering to the principles of clean
architecture means ensuring that your application is easy to test, maintain,
and modernize.

You can read more about this template at the links below:

https://github.com/HeaTTheatR/LoginAppMVC
https://en.wikipedia.org/wiki/Model–view–controller
"""
import json
import asynckivy as ak

from kivy.loader import Loader
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.uix.popup import Popup
from kivy.network.urlrequest import UrlRequest

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
        self.is_finished_loading_data = False
        Window.bind(on_keyboard=self.on_keyboard)

    def build(self) -> MDScreenManager:
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Light"
        # self.theme_cls.primary_palette = "Blue"
        # self.theme_cls.primary_hue = "800"
        # self.theme_cls.primary_light_hue = "50"
        # self.theme_cls.accent_palette = 'BlueGray'
        # self.theme_cls.accent_hue = "900"
        self.theme_cls.colors = colors
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Red"
        self.generate_application_screens()
        ak.start(self.load_data())
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
    
    def show_error(self, req, error):
        popup = ErrorPopup(separator_height=0, title="Ошибка при запуске приложения!",
                              size=(500, 300), size_hint=(None, None))
        popup.open()

    def generate_category_items(self, *args) -> None:
        # req = UrlRequest(self.model.HOST_API + 'categories/', on_error=self.show_error)
        # req.wait()
        # self.model.category_items = req.result
        c_items = []
        
        path_to_c_items = self.model.DATA_DIR.joinpath(
            self.model.DATA_DIR, "category_items.json"
        )
        
        if path_to_c_items.exists():
            with open(path_to_c_items) as json_file:
                c_items = json.loads(json_file.read())
        
        self.model.category_items = c_items

    def generate_items(self, *args) -> None:
        req = UrlRequest(self.model.HOST_API + 'items/')
        req.wait()
        items = req.result
        # append additional fields
        for item in items:
            item['id'] = str(item['id'])
            item['image_count'] = self.model.ITEM_IMAGE_COUNT
            item['is_favorite'] = False
            item['controller'] = self
            # fulltext search field
            s = [item['title'].lower(), item['text'].lower()]
            item['fulltext'] = ('#').join(s)
        self.model.items = items      

    def generate_fav_items(self, *args) -> None:
        f_items = []
        self.model.fav_items = []
        path_to_fav_items = self.model.DATA_DIR.joinpath(
            self.model.DATA_DIR, "fav_items.json"
        )
        if path_to_fav_items.exists():
            with open(path_to_fav_items) as json_file:
                f_items = json.loads(json_file.read())
        fav_items = []
        for item in self.model.items:
            if any(item['id'] == f['id'] for f in f_items):
                item['is_favorite'] = True
                fav_items.append(item)
        self.model.fav_items = fav_items

    def generate_last_items(self, *args) -> None:
        last_items = []
        last_items_count = min(
            self.model.LAST_ITEMS_COUNT, len(self.model.items))
        for i in range(last_items_count):
            last_items.append(self.model.items[i])
        self.model.last_items = last_items
    
    def set_user_settings(self, *args) -> None:
        path_to_settings = self.model.DATA_DIR.joinpath(
            self.model.DATA_DIR, "user_settings.json"
        )
        if path_to_settings.exists():
            with open(path_to_settings) as json_file:
                self.model.user = json.loads(json_file.read())
        self.model.browse_type = self.model.user['browse_type']
    
    async def load_data(self) -> None:
        await ak.sleep(0)
        self.generate_category_items()
        self.generate_items()
        self.generate_fav_items()
        self.generate_last_items()
        self.set_user_settings()
        self.manager_screens.current = 'main screen'
        

ipolice_kivy().run()
