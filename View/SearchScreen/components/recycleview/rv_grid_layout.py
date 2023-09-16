from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

class GridRecycleLayout(FocusBehavior, LayoutSelectionBehavior, RecycleGridLayout):
    pass