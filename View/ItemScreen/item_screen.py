from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from View.base_screen import BaseScreenView
from .components.layout.item_image import ItemImage


class ItemScreenView(BaseScreenView):
    def on_enter(self):
        if self.model.current_item:
            self.ids.title.text = self.model.current_item['title']
            self.ids.text.text = self.model.current_item['text']
            self.ids.date_of_creation.text = 'Добавлен: ' + \
                self.model.current_item['date_of_creation']
            self.ids.date_of_change.text = 'Изменен: ' + \
                self.model.current_item['date_of_change']
            for i in range(self.model.ITEM_IMAGE_COUNT):
                if self.model.current_item['photo' + str(i + 1)]:
                    lt = MDRelativeLayout()
                    lt.add_widget(FitImage(
                        source=self.model.current_item['photo' + str(i + 1)]))
                    fav_button = MDIconButton(
                        icon='heart-outline',
                        pos_hint={'top': 1, 'left': .8},
                        theme_text_color='Custom',
                        text_color='#0072B5')

                    share_button = MDIconButton(
                        icon='share-variant-outline',
                        pos_hint={'top': 1, 'right': 1},
                        theme_text_color='Custom',
                        text_color='#0072B5')

                    counter_label = MDLabel(
                        pos_hint={'center_x': .5, 'bottom': .1},
                        theme_text_color='Custom',
                        text_color='#0072B5')

                    self.ids.carousel.add_widget(fav_button)
                    self.ids.carousel.add_widget(share_button)
                    self.ids.carousel.add_widget(counter_label)

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
