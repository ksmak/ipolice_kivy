from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.properties import StringProperty


class ItemImage(MDRelativeLayout):
    """class for implement item card."""
    image_path = StringProperty()
