from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

class BoxRecycleLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    pass