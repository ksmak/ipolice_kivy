from kivy.properties import (
    NumericProperty,
    StringProperty,
    BooleanProperty,
    ObjectProperty,
)
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.fitimage import FitImage


class GalleryLabel(RecycleDataViewBehavior, MDBoxLayout):
    index = 0
    item_id = StringProperty()
    title = StringProperty()
    text = StringProperty()
    date = StringProperty()
    is_favorite = BooleanProperty()
    image_count = NumericProperty()
    controller = ObjectProperty()
    sliding = False

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.item_id = data['id']
        self.title = data['title']
        self.text = data['text']
        # self.date = data['date_of_creation']
        self.date = str(data['is_favorite'])
        self.is_favorite = data['is_favorite']
        self.controller = data['controller']

        self.ids.carousel.clear_widgets()
        for i in range(data['image_count']):
            if data['photo' + str(i + 1)]:
                lt = MDRelativeLayout()
                image = FitImage(
                    source=data['photo' + str(i + 1)],
                    radius=(12, 12, 0, 0)
                )
                lt.add_widget(image)
                self.ids.carousel.add_widget(lt)

        self.ids.count_info.text = '1/' + str(len(self.ids.carousel.slides))

        self.ids.favorite_button.bind(on_release=self.on_click_favorite_button)

        super(GalleryLabel, self).refresh_view_attrs(rv, index, data)

    def on_click_favorite_button(self, *args):
        self.sliding = True
        self.controller.set_favorite_item(self.item_id)
        self.is_favorite = not self.is_favorite

    def on_touch_up(self, touch):
        # if super(GalleryLabel, self).on_touch_up(touch):
        #     return True
        if self.collide_point(*touch.pos):
            self.parent.select_with_touch(self.index, touch)
            self.parent.clear_selection()
            return False

    def apply_selection(self, rv, index, is_selected):
        if is_selected and not self.sliding:
            self.controller.set_current_item(rv.data[index]['id'])
            self.controller.view.manager_screens.current = 'item screen'
        else:
            self.sliding = False
