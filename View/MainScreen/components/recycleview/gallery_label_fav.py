from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty,
    ObjectProperty,
)
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.fitimage import FitImage


class GalleryLabelFav(RecycleDataViewBehavior, MDBoxLayout):
    index = 0
    item_id = NumericProperty()
    title = StringProperty()
    text = StringProperty()
    date = StringProperty()
    image_count = NumericProperty()
    real_count = 0
    is_favorite = BooleanProperty()
    controller = ObjectProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.item_id = data['item_id']
        self.title = data['title']
        self.text = data['text']
        self.date = data['date']
        self.image_count = data['image_count']
        self.is_favorite = data['is_favorite']
        self.controller = data['controller']

        self.ids.carousel_fav.clear_widgets()
        self.real_count = 0
        for i in range(self.image_count):
            if data['photo' + str(i + 1)]:
                lt = MDRelativeLayout()
                lt.add_widget(FitImage(source=data['photo' + str(i + 1)]))
                self.ids.carousel_fav.add_widget(lt)
                self.real_count = self.real_count + 1

        self.ids.count_info_fav.text = '1/' + str(self.real_count)
        self.ids.favorite_button_fav.bind(on_release=self.on_click_favorite_button)

        super(GalleryLabel, self).refresh_view_attrs(rv, index, data)

    def on_click_favorite_button(self, *args):
        if self.is_favorite:
            self.controller.unset_favorite_item(self.item_id)
        else:
            self.controller.set_favorite_item(self.item_id)
        
        self.is_favorite = not self.is_favorite