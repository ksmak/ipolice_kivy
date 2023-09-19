"""
The entry point to the application.

The application uses the MVC template. Adhering to the principles of clean
architecture means ensuring that your application is easy to test, maintain,
and modernize.

You can read more about this template at the links below:

https://github.com/HeaTTheatR/LoginAppMVC
https://en.wikipedia.org/wiki/Model–view–controller
"""
from pathlib import Path

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from kivy.loader import Loader
from kivy.logger import Logger

from View.screens import screens, main_model

Loader.num_workers = 4



class ipolice_kivy(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # constants
        self.BASE_DIR = Path(__file__).resolve().parent
        Logger.info('python BASE_DIR=%s', self.BASE_DIR)
        self.DATA_DIR = self.BASE_DIR.joinpath("assets", "data")
        Logger.info('python DATA_DIR=%s', self.DATA_DIR)
        self.ITEM_IMAGE_COUNT = 5
        self.LAST_ITEMS_COUNT = 10
        # load kv
        self.load_all_kv_files(self.directory)
        # This is the screen manager that will contain all the screens of your
        # application.
        self.manager_screens = MDScreenManager()

    def refresh_recycleview(self, gallery_rv, list_rv, grid_rv, items, favorite_items, controller):
        data = []
        for item in items:
            data.append({
                'item_id': item['id'],
                'title': item['title'],
                'text': item['text'],
                'date': item['date_of_creation'],
                'photo1': (str(self.BASE_DIR) + '/' + item['photo1']) if item['photo1'] else None,
                'photo2': (str(self.BASE_DIR) + '/' + item['photo2']) if item['photo2'] else None,
                'photo3': (str(self.BASE_DIR) + '/' + item['photo3']) if item['photo3'] else None,
                'photo4': (str(self.BASE_DIR) + '/' + item['photo4']) if item['photo4'] else None,
                'photo5': (str(self.BASE_DIR) + '/' + item['photo5']) if item['photo5'] else None,
                'image_count': self.ITEM_IMAGE_COUNT,
                'is_favorite': any(item['id'] == d['id'] for d in favorite_items),
                'controller': controller,
            })
        gallery_rv.data = data
        gallery_rv.refresh_from_data()
        list_rv.data = data
        list_rv.refresh_from_data()
        grid_rv.data = data
        grid_rv.refresh_from_data()

    def build(self) -> MDScreenManager:
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "800"
        self.theme_cls.primary_light_hue = "50"
        self.theme_cls.accent_palette = 'DeepOrange'
        self.theme_cls.accent_hue = "900"
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

        model = main_model(self.DATA_DIR, self.LAST_ITEMS_COUNT)

        for i, name_screen in enumerate(screens.keys()):
            # model = screens[name_screen]["model"]()
            controller = screens[name_screen]["controller"](model)
            view = controller.get_view()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)


ipolice_kivy().run()
