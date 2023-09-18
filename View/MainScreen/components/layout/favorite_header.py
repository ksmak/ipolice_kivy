from kivy.properties import StringProperty

from kivymd.uix.boxlayout import MDBoxLayout


class FavoriteHeader(MDBoxLayout):
    title = StringProperty()
    button = StringProperty('gallery')
