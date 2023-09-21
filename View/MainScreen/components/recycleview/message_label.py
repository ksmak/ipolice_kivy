from kivy.properties import (
    NumericProperty,
    StringProperty,
    BooleanProperty,
    ObjectProperty,
)
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior


class MessageLabel(RecycleDataViewBehavior, MDBoxLayout):
    index = 0
    is_own = BooleanProperty()
    from_id = NumericProperty()
    to_id = NumericProperty()
    text = StringProperty()
    date = StringProperty()
    is_send = BooleanProperty()
    is_read = BooleanProperty()
    controller = ObjectProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.item_id = data['id']
        self.is_own = data['is_own']
        self.from_id = data['from_id']
        self.to_id = data['to_id']
        self.text = data['text']
        self.date = data['date_of_creation']
        self.is_send = data['is_send']
        self.is_read = data['is_read']
        self.controller = data['controller']

        super(MessageLabel, self).refresh_view_attrs(rv, index, data)

    def remove_message(self):
        self.controller.remove_message(self.item_id)
