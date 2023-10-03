from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior

from kivymd.uix.boxlayout import MDBoxLayout


class CategoryItem(ButtonBehavior, MDBoxLayout):
    photo = StringProperty()
    title = StringProperty()
    text = StringProperty()
