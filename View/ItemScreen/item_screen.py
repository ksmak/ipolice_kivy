from plyer import call
from jnius import cast
from jnius import autoclass

from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.image import AsyncImage
from kivy.utils import platform

from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFloatingActionButtonSpeedDial

from View.base_screen import BaseScreenView
from Utility.helper import get_by_id


class ItemScreenView(BaseScreenView):
    is_favorite = BooleanProperty()
    target_screen = StringProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.data = {'Позвонить': [
            'phone',
            'on_release', lambda x: self.call_phone(),
        ],
            'Написать': [
            'whatsapp',
            'on_release', lambda x: self.send_message(),
        ]}

        self.float_button = None

    def create_floating_button(self):
        if self.float_button:
            self.remove_widget(self.float_button)

        self.float_button = MDFloatingActionButtonSpeedDial(
            icon="card-account-phone",
            label_text_color="white",
            hint_animation=True,
            bg_hint_color=self.app.theme_cls.primary_dark,
            bg_color_root_button=self.app.theme_cls.primary_color,
            bg_color_stack_button=self.app.theme_cls.primary_color,
            data=self.data
        )

        self.add_widget(self.float_button)

    def on_pre_enter(self):
        self.app.target_screen = self.model.target_screen
        self.ids.title.text = self.model.current_item['title']
        self.ids.place_info.text = self.model.current_item['place_info_with_date']
        self.ids.text.text = self.model.current_item['text']

        self.ids.carousel.clear_widgets()
        for i in range(self.model.ITEM_IMAGE_COUNT):
            if self.model.current_item['photo' + str(i + 1)]:
                lt = MDRelativeLayout()
                image = AsyncImage(
                    source=self.model.current_item['photo' + str(i + 1)],
                    fit_mode='fill')
                lt.add_widget(image)
                self.ids.carousel.add_widget(lt)

        self.ids.counter.text = str(
            self.ids.carousel.index + 1) + '/' + str(len(self.ids.carousel.slides))
        category = get_by_id(
            self.model.current_item['category'], self.model.category_items)

        self.ids.details_container.clear_widgets()
        for field in category['fields']:
            if self.model.current_item[field]:
                txt: str
                if category['fields'][field]['type'] == 'text':
                    txt = str(self.model.current_item[field])
                else:
                    txt = self.model.current_item[field]['title']
                label = MDLabel(
                    text=category['fields'][field]['title'] + ': ' + txt,
                    font_style='Caption',
                    text_color='white',
                    theme_text_color='Custom',
                    padding='2dp',
                    adaptive_size=True

                )
                label.md_bg_color = (
                    # 40 / 255, 24 / 255, 177 / 255)
                    16 / 255, 122 / 255, 94 / 255)

                self.ids.details_container.add_widget(label)

        self.is_favorite = any(
            self.model.current_item['id'] == d['id'] for d in self.model.fav_items)
        self.ids.favorite_button.bind(on_release=self.on_click_favorite_button)

        self.ids.date_add.text = self.model.current_item['date_add']

        self.create_floating_button()

    def on_click_favorite_button(self, *args):
        self.controller.set_favorite_item(self.model.current_item['id'])
        self.is_favorite = not self.is_favorite

    def send_message(self, *args):
        if platform == 'android':
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            intent = Intent()
            intent.setAction(Intent.ACTION_VIEW)
            intent.setData(Uri.parse(
                'https://api.whatsapp.com/send?phone='+self.model.current_item['author']['phone']))
            currentActivity = cast(
                'android.app.Activity', PythonActivity.mActivity)
            currentActivity.startActivity(intent)

    def call_phone(self, *args):
        if platform == 'android':
            call.makecall(self.model.current_item['author']['phone'])

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
