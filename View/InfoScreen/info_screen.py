from kivy.properties import StringProperty
from kivy.cache import Cache

from kivy.uix.image import Image
from View.base_screen import BaseScreenView


def change_fit_mode(obj):
    obj.fit_mode = 'fill'


class InfoScreenView(BaseScreenView):
    image_path = StringProperty()

    def __init__(self, **kw):
        super().__init__(**kw)

    def on_pre_enter(self) -> None:
        self.app.screen_stack.append('info screen')
        self.image_path = self.model.current_info['photo1']
        self.ids.photo.bind(on_load=change_fit_mode)
        if Cache.get('kv.loader', self.model.current_info['photo1']):
            self.ids.photo.fit_mode = 'fill'
        self.ids.title.text = self.model.current_info['title']
        self.ids.text.text = self.model.current_info['text']
        self.ids.date_add.text = self.model.current_info['date_add']

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
