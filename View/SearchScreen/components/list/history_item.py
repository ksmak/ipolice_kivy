from kivy.properties import StringProperty
from kivymd.uix.list import OneLineAvatarIconListItem


class HistoryItem(OneLineAvatarIconListItem):
    """The class implements the search history item."""
    title = StringProperty()
