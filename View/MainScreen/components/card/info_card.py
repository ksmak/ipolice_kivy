from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty


class InfoCard(MDBoxLayout):
    """The class implements the info card."""
    icon = StringProperty()
    title = StringProperty()
