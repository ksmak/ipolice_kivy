from datetime import datetime
from plyer import call

from kivy.properties import BooleanProperty, StringProperty
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex

from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout


from View.base_screen import BaseScreenView
from Utility.helper import get_by_id, format_date


class ItemScreenView(BaseScreenView):
    is_favorite = BooleanProperty()
    target_screen = StringProperty()

    def on_pre_enter(self):
        self.app.target_screen = self.model.target_screen
        self.ids.title.text = self.model.current_item['title']
        self.ids.text.text = self.model.current_item['text']
                   
        self.ids.carousel.clear_widgets()
        for i in range(self.model.ITEM_IMAGE_COUNT):
            if self.model.current_item['photo' + str(i + 1)]:
                lt = MDRelativeLayout()
                image = FitImage(source=self.model.current_item['photo' + str(i + 1)])
                lt.add_widget(image)
                self.ids.carousel.add_widget(lt)
            
        self.ids.counter.text = str(self.ids.carousel.index + 1) + '/' + str(len(self.ids.carousel.slides))
        category = get_by_id(self.model.current_item['category'], self.model.category_items)
        
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
                    theme_text_color='Custom',
                    text_color=self.app.theme_cls.primary_color,
                    adaptive_height=True
                )

                self.ids.details_container.add_widget(label)

        self.is_favorite = any(self.model.current_item['id'] == d['id'] for d in self.model.fav_items)
        self.ids.favorite_button.bind(on_release=self.on_click_favorite_button)

        dt = datetime.strptime(self.model.current_item['date_of_creation'], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.ids.date_of_creation.text = 'Добавлен: ' + format_date(dt)
        
        dt = datetime.strptime(self.model.current_item['date_of_change'], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.ids.date_of_change.text = 'Изменен: ' + format_date(dt)
    
    def on_click_favorite_button(self, *args):
        self.controller.set_favorite_item(self.model.current_item['id'])
        self.is_favorite = not self.is_favorite

    def create_message(self, *args):
        # data = {}
        # data['id'] = '0'
        # data['is_own'] = True
        # data['from_id'] = self.model.user_id
        # data['to_id'] = self.model.current_item['author']
        # data['text'] = ''
        # data['date_of_creation'] = ''
        # data['date_of_send'] = ''
        # data['date_of_read'] = ''
        # data['is_send'] = False
        # data['is_read'] = False
        # data['controller'] = self.controller
        # self.controller.set_current_message(data)
        # self.manager_screens.current = 'message screen'
        pass
    
    def call_phone(self, *args):
        # call.makecall(tel=self.model.current_item['phone'])
        pass

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
