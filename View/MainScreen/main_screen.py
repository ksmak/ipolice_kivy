from functools import partial

from kivymd.uix.segmentedbutton import MDSegmentedButton, MDSegmentedButtonItem

from View.base_screen import BaseScreenView
from .components.card.category_card import CategoryCard
from View.SearchScreen.components.recycleview.gallery_label import GalleryLabel
from View.SearchScreen.components.recycleview.list_label import ListLabel
from View.SearchScreen.components.recycleview.grid_label import GridLabel
from View.SearchScreen.components.recycleview.rv_box_layout import BoxRecycleLayout
from View.SearchScreen.components.recycleview.rv_grid_layout import GridRecycleLayout


class MainScreenView(BaseScreenView):
    def on_enter(self):
        self.ids.category_list_container.clear_widgets()
        self.generate_category_cards()
        self.refresh_recycleview()
        self.update_browse_type_button()

    def generate_category_cards(self):
        for category in self.model.category_description:
            card = CategoryCard(
                category_icon=category['icon'],
                category_name=category['name']
            )
            callback_function = partial(self.open_category_items, category['id'])
            card.ids.card_button.bind(on_release=callback_function)
            self.ids.category_list_container.add_widget(card)
    
    def open_category_items(self, category: int, *args) -> None:
        self.controller.search_by_category(category)
        self.manager_screens.current = 'search screen'

    def to_search_screen(self):
        self.controller.open_search()
        self.manager_screens.current = 'search screen'
    
    def refresh_recycleview(self):
        data = []
        for item in self.model.last_items:
            data.append({
                'title': item['title'],
                'text': item['text'],
                'date': item['date_of_creation'],
                'photo1': item['photo1'],
                'photo2': item['photo2'],
                'photo3': item['photo3'],
                'photo4': item['photo4'],
                'photo5': item['photo5'],
                'image_count': self.model.ITEM_IMAGE_COUNT,
            })
        self.ids.gallery_rv.data = data
        self.ids.gallery_rv.refresh_from_data()
        self.ids.list_rv.data = data
        self.ids.list_rv.refresh_from_data()
        self.ids.grid_rv.data = data
        self.ids.grid_rv.refresh_from_data()
    
    def update_browse_type_button(self):
        if self.model.browse_type == 'gallery':
            self.ids.browse_type_button.mark_item(self.ids.gallery_button)
            self.ids.gallery_rv.opacity = 1
            self.ids.list_rv.opacity = 0
            self.ids.grid_rv.opacity = 0
        elif self.model.browse_type == 'list':
            self.ids.browse_type_button.mark_item(self.ids.list_button)
            self.ids.gallery_rv.opacity = 0
            self.ids.list_rv.opacity = 1
            self.ids.grid_rv.opacity = 0
        elif self.model.browse_type == 'grid':
            self.ids.browse_type_button.mark_item(self.ids.grid_button)
            self.ids.grid_button.active = True
            self.ids.gallery_rv.opacity = 0
            self.ids.list_rv.opacity = 0
            self.ids.grid_rv.opacity = 1
    
    def set_browse_type(
        self, 
        segment_button: MDSegmentedButton, 
        segment_item: MDSegmentedButtonItem, 
        marked: bool) -> None:

        if segment_item.icon == 'view-gallery-outline':
            self.controller.set_browse_type('gallery')
        elif segment_item.icon == 'view-list-outline':
            self.controller.set_browse_type('list')
        elif segment_item.icon == 'view-grid-outline':
            self.controller.set_browse_type('grid')

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
        self.update_browse_type_button()
        
