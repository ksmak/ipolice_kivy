from kivymd.uix.card import MDCard
from kivy.properties import StringProperty


class InfoCard(MDCard):
    """The class implements the info card."""
    icon = StringProperty()
    title = StringProperty()
