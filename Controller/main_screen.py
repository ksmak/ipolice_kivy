import json
import asynckivy as ak
import dateutil.parser

from kivy.network.urlrequest import UrlRequest
from kivy.logger import Logger

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from View.MainScreen.main_screen import MainScreenView
from Utility.helper import save_file, format_date, format_date_without_time


class MainScreenController:
    """
    Main screen controller.
    """
    error_dialog = None

    def __init__(self, model):
        self.model = model
        self.view = MainScreenView(controller=self, model=self.model)

    def get_view(self) -> MainScreenView:
        return self.view

    def on_load_data_error(self, req, error):
        Logger.info("Error loading data.")
        self.view.app.show_error()

    async def generate_info_items(self, *args) -> None:
        ak.sleep(0)

        self.model.info_result = False

        def get_result(req, result):
            info_items = req.result
            # append additional fields
            for item in info_items:
                item['id'] = str(item['id'])
                item['item_type'] = 'info'
                item['image_count'] = 1
                item['is_favorite'] = False
                item['controller'] = self
                item['date'] = format_date(
                    dateutil.parser.isoparse(item['date_of_creation']))
                item['date_add'] = 'Добавлен: ' + format_date(
                    dateutil.parser.isoparse(item['date_of_creation']))
                item['place_info'] = ''
                item['place_info_with_date'] = item['date']

            self.model.info_items = info_items
            self.view.generate_info_cards()
            self.info_result = True
            self.model.notify_observers()

        req = UrlRequest(
            self.model.HOST_API + 'info/',
            on_success=get_result,
            on_error=self.on_load_data_error,
            on_failure=self.on_load_data_error
        )

        # req.wait()

    async def generate_category_items(self, *args) -> None:
        ak.sleep(0)

        self.model.category_result = False

        def get_result(req, result):
            self.model.category_items = req.result
            self.view.generate_category_cards()
            self.model.category_result = True
            self.model.notify_observers()

        req = UrlRequest(
            self.model.HOST_API + 'categories/',
            on_success=get_result,
            on_error=self.on_load_data_error,
            on_failure=self.on_load_data_error
        )

        # req.wait()

    async def generate_items(self, *args) -> None:
        ak.sleep(0)

        self.model.items_result = False

        def get_result(req, result):
            items = req.result
            # append additional fields
            for item in items:
                item['id'] = str(item['id'])
                item['item_type'] = 'item'
                item['image_count'] = self.model.ITEM_IMAGE_COUNT
                item['is_favorite'] = False
                item['controller'] = self
                item['fulltext'] = ('#').join(
                    [item['title'].lower(), item['text'].lower()])
                item['date'] = dateutil.parser.isoparse(
                    item['date_of_action']).strftime('%d.%m.%Y')
                item['date_add'] = 'Добавлен: ' + format_date(
                    dateutil.parser.isoparse(item['date_of_creation']))
                item['place_info'] = ", ".join(
                    [item['region'].get('title', ''), item['district'].get('title', '') if item['district'] else '', item['punkt']])
                item['place_info_with_date'] = ", ".join(
                    [item['region'].get('title', ''), item['district'].get('title', '') if item['district'] else '', item['punkt'], item['date']])
            self.model.items = items
            self.generate_fav_items()
            self.generate_last_items()
            self.view.refresh_data_items()
            self.model.items_result = True
            self.model.notify_observers()

        req = UrlRequest(
            self.model.HOST_API + 'items/',
            on_success=get_result,
            on_error=self.on_load_data_error,
            on_failure=self.on_load_data_error
        )

        # req.wait()

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

    async def set_user_settings(self, *args) -> None:
        ak.sleep(0)
        path_to_settings = self.model.DATA_DIR.joinpath(
            self.model.DATA_DIR, "user_settings.json"
        )
        if path_to_settings.exists():
            with open(path_to_settings) as json_file:
                self.model.user = json.loads(json_file.read())
        try:
            self.model.browse_type = self.model.user['browse_type']
        except:
            self.model.browse_type = 'list'

    def set_browse_type(self, browse_type: str, *args) -> None:
        self.model.browse_type = browse_type
        self.model.user['browse_type'] = browse_type
        save_file(self.model.DATA_DIR, 'user_settings.json', self.model.user)

    def search_by_category(self, category: int) -> None:
        async def search() -> None:
            find_items = []
            for item in self.model.items:
                if (item['category'] == category):
                    find_items.append(item)
                await ak.sleep(0)
            self.model.find_items = find_items
            self.model.is_loading = False
            self.model.notify_observers()

        self.model.is_first_open = False
        self.model.is_loading = True
        self.model.find_items = []

        ak.start(search())

    def open_search(self):
        self.model.current_category = {}
        self.model.find_items = []
        self.model.is_first_open = True

    def set_favorite_item(self, id: int) -> None:
        res = [d for d in self.model.items if d['id'] == id]
        if res:
            res[0]['is_favorite'] = not res[0]['is_favorite']
            if res[0] not in self.model.fav_items and res[0]['is_favorite']:
                self.model.fav_items.append(res[0])
            else:
                self.model.fav_items.remove(res[0])
            fav_items = []
            for item in self.model.fav_items:
                fav_items.append({'id': item['id']})
            save_file(self.model.DATA_DIR, "fav_items.json", fav_items)

    def set_current_item(self, id: int) -> None:
        res = [d for d in self.model.items if d['id'] == id]
        if res:
            self.model.current_item = res[0]

    def set_current_info(self, id: int) -> None:
        res = [d for d in self.model.info_items if d['id'] == id]
        if res:
            self.model.current_info = res[0]

    def set_current_category(self, id: int) -> None:
        res = [d for d in self.model.category_items if d['id'] == id]
        if res:
            self.model.current_category = res[0]
