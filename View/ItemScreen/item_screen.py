from kivy.metrics import dp
from kivy.properties import BooleanProperty, StringProperty

from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.fitimage import FitImage
from kivymd.uix.button import MDIconButton
from kivymd.uix.chip import MDChip, MDChipText

from View.base_screen import BaseScreenView
from Utility.helper import get_by_id


class ItemScreenView(BaseScreenView):
    is_favorite = BooleanProperty()
    target_screen = StringProperty()

    def on_pre_enter(self):
        if self.model.current_item:
            
            self.ids.title.text = self.model.current_item['title']
            
            self.ids.text.text = self.model.current_item['text']
            
            self.ids.date_of_creation.text = 'Добавлен: ' + \
                self.model.current_item['date_of_creation']
            
            self.ids.date_of_change.text = 'Изменен: ' + \
                self.model.current_item['date_of_change']
            
            self.ids.carousel.clear_widgets()
            for i in range(self.app.ITEM_IMAGE_COUNT):
                if self.model.current_item['photo' + str(i + 1)]:
                    lt = MDRelativeLayout()
                    image = FitImage(source=self.model.current_item['photo' + str(i + 1)])
                    lt.add_widget(image)
                    self.ids.carousel.add_widget(lt)
            
            self.ids.counter.text = str(self.ids.carousel.index + 1) + '/' + str(len(self.ids.carousel.slides))

            self.ids.details_container.clear_widgets()
            category = get_by_id(self.model.current_item['category'], self.model.category_description)
            for field in category['fields']:
                chidp_text = MDChipText(
                    text=category['fields_desc'][field] + ': ' + self.model.current_item[field],
                    theme_text_color='Custom',
                    text_color='#ffffff',
                    font_style='Caption')
                chip = MDChip(
                    type="assist",
                    md_bg_color='#10739E')
                chip.add_widget(chidp_text)
                self.ids.details_container.add_widget(chip)
            
            self.is_favorite = any(self.model.current_item['id'] == d['id'] for d in self.model.favorite_items)
            self.ids.favorite_button.bind(on_release=self.on_click_favorite_button)
        
        self.target_screen = self.model.target_screen
    
    def on_click_favorite_button(self, *args):
        if self.is_favorite:
            self.controller.unset_favorite_item(self.model.current_item['id'])
        else:
            self.controller.set_favorite_item(self.model.current_item['id'])
        
        self.is_favorite = not self.is_favorite

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
