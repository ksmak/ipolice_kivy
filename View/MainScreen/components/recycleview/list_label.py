from kivy.properties import (
    StringProperty,
    BooleanProperty,
    ObjectProperty,
)
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior


class ListLabel(RecycleDataViewBehavior, MDBoxLayout):
    index = 0
    item_id = StringProperty()
    photo = StringProperty()
    title = StringProperty()
    text = StringProperty()
    place_info = StringProperty()
    is_favorite = BooleanProperty()
    controller = ObjectProperty()
    sliding = False
    item_type = StringProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.item_id = data['id']
        self.photo = data['photo1'] if data['photo1'] else ''
        self.title = data['title']
        self.text = data['text']
        self.item_type = data['item_type']
        self.date = data['date']
        self.place_info = data['place_info_with_date']
        self.is_favorite = data['is_favorite']
        self.controller = data['controller']

        if self.item_type == 'item':
            self.ids.favorite_button.opacity = 1
            self.ids.favorite_button.bind(
                on_release=self.on_click_favorite_button)
        else:
            self.ids.favorite_button.opacity = 0

        super(ListLabel, self).refresh_view_attrs(rv, index, data)

    def on_click_favorite_button(self, *args):
        self.sliding = True
        self.controller.set_favorite_item(self.item_id)
        self.is_favorite = not self.is_favorite

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.parent.select_with_touch(self.index, touch)
            self.parent.clear_selection()
            return False

    def apply_selection(self, rv, index, is_selected):
        if is_selected and not self.sliding:
            if rv.data[index]['item_type'] == 'item':
                self.controller.set_current_item(rv.data[index]['id'])
                self.controller.view.manager_screens.current = 'item screen'
            elif rv.data[index]['item_type'] == 'info':
                self.controller.set_current_info(rv.data[index]['id'])
                self.controller.view.manager_screens.current = 'info screen'
        else:
            self.sliding = False
