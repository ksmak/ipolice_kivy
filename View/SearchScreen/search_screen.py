from functools import partial

from kivymd.uix.segmentedbutton import MDSegmentedButton, MDSegmentedButtonItem

from View.base_screen import BaseScreenView
from .components.list.search_history_item import SearchHistoryItem
from .components.recycleview.gallery_label import GalleryLabel
from .components.recycleview.list_label import ListLabel
from .components.recycleview.grid_label import GridLabel
from .components.recycleview.rv_box_layout import BoxRecycleLayout
from .components.recycleview.rv_grid_layout import GridRecycleLayout



class SearchScreenView(BaseScreenView):
    def on_enter(self):
        self.generate_search_history_items()
        self.refresh_recycleview()

    def generate_search_history_items(self):
        self.ids.search_history_container.clear_widgets()
        for history_item in self.model.search_history_description:
            item = SearchHistoryItem(
                title=history_item['title']
            )
            callback_function = partial(self.history_search, history_item['title'])
            item.bind(on_press=callback_function)
            callback_function = partial(self.remove_search_history_item, history_item)
            item.ids.search_history_icon.bind(on_press=callback_function)
            self.ids.search_history_container.add_widget(item)
    
    def remove_search_history_item(self, item, instance):
        self.controller.remove_search_history_item(item)
    
    def remove_all_search_history_items(self):
        self.controller.remove_all_search_history_items()
    
    def history_search(self, sf: str, *args):
        self.ids.search_field.text = sf
        self.controller.search(sf.lower())
    
    def search(self):
        self.controller.search(self.ids.search_field.text.lower())
    
    def refresh_recycleview(self):
        data = []
        for item in self.model.find_items:
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
        self.ids.loading.active = self.model.search_loading
        
        if self.model.is_first_search or not self.model.search_history_description:
            self.ids.history_layout.opacity = 0
            self.ids.search_history_container.opacity = 0
        else:
            self.ids.history_layout.opacity = 1
            self.ids.search_history_container.opacity = 1
            self.generate_search_history_items()   
        
        if self.model.is_first_search and self.model.search_loading == False:
            self.ids.result_layout.opacity = 1
            self.refresh_recycleview()
            self.ids.result_count.text = 'Найдено: ' + str(len(self.model.find_items))
        else:
            self.ids.result_layout.opacity = 0
        
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

            
        
