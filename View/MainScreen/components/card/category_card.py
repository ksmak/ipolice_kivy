from kivymd.uix.card import MDCard
from kivy.properties import StringProperty


class CategoryCard(MDCard):
    """The class implements the category card."""
    category_icon = StringProperty()
    category_name = StringProperty()