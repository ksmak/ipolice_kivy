from kivy.properties import (
    StringProperty,
    NumericProperty,
    ObjectProperty,
    BooleanProperty,
)
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior


class ListLabel(RecycleDataViewBehavior, MDBoxLayout):
    index = 0
    item_id = NumericProperty()
    title = StringProperty()
    text = StringProperty()
    date = StringProperty()
    image_path = StringProperty()
    is_favorite = BooleanProperty()
    controller = ObjectProperty()
    sliding = False

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.item_id = data['item_id']
        self.title = data['title']
        self.text = data['text']
        self.date = data['date']
        self.image_path = data['photo1']
        self.is_favorite = data['is_favorite']
        self.controller = data['controller']

        self.ids.favorite_button.bind(on_release=self.on_click_favorite_button)

        super(ListLabel, self).refresh_view_attrs(rv, index, data)
    
    def on_click_favorite_button(self, *args):
        self.sliding = True
        if self.is_favorite:
            self.controller.unset_favorite_item(self.item_id)
        else:
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
            self.controller.set_current_item(rv.data[index]['item_id'])
            self.controller.view.manager_screens.current = 'item screen'
        else:
            self.sliding = False
