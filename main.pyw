from kivy.app import App

from kivy.uix.screenmanager import ScreenManager, SlideTransition, Screen

from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.button import Button

from kivy.config import Config
Config.set("graphics", "fullscreen", "auto")

def switch_screen(id):
    global sm, screens
    sm.switch_to(screens[id])

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
        self.add_widget(Button())

if __name__ == "__main__":
    SpotifyController().run()

