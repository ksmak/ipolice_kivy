"""
The entry point to the application.

The application uses the MVC template. Adhering to the principles of clean
architecture means ensuring that your application is easy to test, maintain,
and modernize.

You can read more about this template at the links below:

https://github.com/HeaTTheatR/LoginAppMVC
https://en.wikipedia.org/wiki/Model–view–controller
"""

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button

from View.screens import screens, main_model

class ConfirmationPopup(Popup):
    def __init__(self, **kwargs):
        super(ConfirmationPopup, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')
        label = Label(text='Are you sure you want to exit?')
        button_layout = BoxLayout(orientation='horizontal')

        button_ok = Button(text='Ok', size_hint=(0.5, 1))
        button_ok.bind(on_press=self.confirm)
        button_cancel = Button(text='Cancel', size_hint=(0.5, 1))
        button_cancel.bind(on_press=self.dismiss)

        button_layout.add_widget(button_ok)
        button_layout.add_widget(button_cancel)
        layout.add_widget(label)
        layout.add_widget(button_layout)

        self.content = layout

    def confirm(self, instance):
        MDApp.get_running_app().stop()

class MyInstance(BoxLayout):
    pass

class ipolice_kivy(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(self.directory)
        # This is the screen manager that will contain all the screens of your
        # application.
        self.manager_screens = MDScreenManager()
        
        buttons = [
            MDFlatButton(
                text="Закрыть",
                theme_text_color="Custom",
                text_color=self.theme_cls.primary_color,
            ),
            MDFlatButton(
                text="Отмена",
                theme_text_color="Custom",
                text_color=self.theme_cls.primary_color,
            ),
        ]
        
        buttons[0].bind(on_release=self.set_close_state)
        
        self.close_app_dialog = MDDialog(
            text="Закрыть приложение?",
            buttons=buttons,
        )

        self.close_state = True
        
    def build(self) -> MDScreenManager:
        self.generate_application_screens()
        return self.manager_screens
    
    def on_stop(self):
        if self.close_state:
            self.close_app_dialog.open()
        
        return self.close_state
    
    def set_close_state(self):
        self.close_state = True

    def generate_application_screens(self) -> None:
        """
        Creating and adding screens to the screen manager.
        You should not change this cycle unnecessarily. He is self-sufficient.

        If you need to add any screen, open the `View.screens.py` module and
        see how new screens are added according to the given application
        architecture.
        """

        model = main_model()

        for i, name_screen in enumerate(screens.keys()):
            # model = screens[name_screen]["model"]()
            controller = screens[name_screen]["controller"](model)
            view = controller.get_view()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)


ipolice_kivy().run()
