from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.fitimage import FitImage


class GalleryLabel(RecycleDataViewBehavior, MDBoxLayout):
    index = 0
    title = StringProperty()
    text = StringProperty()
    date = StringProperty()
    image_count = NumericProperty()
    real_count = 0

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.title = data['title']
        self.text = data['text']
        self.date = data['date']
        self.image_count = data['image_count']

        self.ids.carousel.clear_widgets()
        self.real_count = 0
        for i in range(self.image_count):
            if data['photo' + str(i + 1)]:
                lt = MDRelativeLayout()
                lt.add_widget(FitImage(source=data['photo' + str(i + 1)]))
                self.ids.carousel.add_widget(lt)
                self.real_count = self.real_count + 1

        self.ids.count_info.text = '1/' + str(self.real_count)

        super(GalleryLabel, self).refresh_view_attrs(rv, index, data)
