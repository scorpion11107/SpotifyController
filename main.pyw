import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"

from core import load_spotify, get_playlists

from kivy.app import App

from kivy.uix.screenmanager import ScreenManager, SlideTransition, Screen

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage

from kivy.config import Config
Config.set("graphics", "fullscreen", "auto")

def switch_screen(id):
    global sm, screens
    sm.switch_to(screens[id])

sp = load_spotify()

def get_user_playlists():
    global up
    up = get_playlists(sp)

class SpotifyController (App):
    def build(self):
        return MainScreen()

class MainScreen (Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        layout = FloatLayout()
        layout.add_widget(Header())

        global sm
        sm = ScreenManager(transition = SlideTransition(duration = 0.2),
                           size_hint = (1, 0.9),
                           pos_hint = {"x": 0, "y": 0})
        
        global screens
        screens = []

        screens.append(HomeScreen())

        switch_screen(0)

        self.add_widget(layout)
        self.add_widget(sm)

class Header (GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = [1, 0.1]
        self.pos_hint = {"x": 0, "y": 0.9}

        self.add_widget(HomeButton())
        self.add_widget(CloseButton())

        self.cols = len(self.children)

class CloseButton (Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Close"
        self.bind(on_press = exit)
        self.size_hint_x = None
        self.width = 200

class HomeButton (Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Home"

class HomeScreen (Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        
        layout = GridLayout(size_hint = [1, 1])

        get_user_playlists()
        for p in up:
            layout.add_widget(PlaylistButton(p = p))
        
        layout.cols = 3

        self.add_widget(layout)

class PlaylistButton(ButtonBehavior, BoxLayout):
    def __init__(self, p, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'  # Arrange content horizontally
        self.spacing = 10
        self.padding = 10
        self.size_hint = (1, 1)  # Stretch horizontally but not vertically
        self.height = 50  # Fixed height for the button
        
        # Add an image to the button
        self.img = AsyncImage(source=p[1], size_hint = [None, None], size = (self.height, self.height))
        self.add_widget(self.img)
        
        # Add a label to the button
        lbl = Label(text = p[0], halign = 'left', valign = 'middle', size_hint = (1, 1))
        lbl.bind(size=lbl.setter('text_size'))
        self.add_widget(lbl)

        self.bind(height = self._update_image_size)
    
    def _update_image_size(self, *args):
        """Ensure the image's size matches the height of the button."""
        self.img.size = (self.height*0.9, self.height*0.9)

if __name__ == "__main__":
    SpotifyController().run()

