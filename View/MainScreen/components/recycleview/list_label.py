from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior


class ListLabel(RecycleDataViewBehavior, MDBoxLayout):
    title = StringProperty()
    text = StringProperty()
    date = StringProperty()
    image_path = StringProperty()
    index = None

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.title = data['title']
        self.text = data['text']
        self.date = data['date']
        self.image_path = data['photo1']

        super(ListLabel, self).refresh_view_attrs(rv, index, data)
