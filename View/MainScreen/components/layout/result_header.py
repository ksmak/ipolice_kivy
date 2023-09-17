from kivy.properties import StringProperty

from kivymd.uix.boxlayout import MDBoxLayout


class ResultHeader(MDBoxLayout):
    title = StringProperty()
    button = StringProperty('gallery')
