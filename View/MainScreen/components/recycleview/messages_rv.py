from kivy.properties import (
    NumericProperty,
    StringProperty,
    BooleanProperty,
    ObjectProperty
)
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior

class MessageLabel(RecycleDataViewBehavior, MDBoxLayout):
    index = 0
    msg_id = NumericProperty()
    from_id = NumericProperty()
    text = StringProperty()
    date_of_creation = StringProperty()
    is_send = BooleanProperty()
    is_read = BooleanProperty()
    is_own = BooleanProperty()
    controller = ObjectProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.msg_id = data['msg_id']
        self.from_id = data['from_id']
        self.text = data['text']
        self.date_of_creation = data['date_of_creation']
        self.is_send = data['is_send']
        self.is_read = data['is_read']
        self.is_own = data['is_own']
        self.controller = data['controller']
        super(MessageLabel, self).refresh_view_attrs(rv, index, data)
    
    def remove_message(self):
        self.controller.remove_message(self.msg_id)