import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window


class CreateDiceScreen(Screen):
    """ The creation of the dice """
    pass
    
class CreateDicesSetScreen(Screen):
    """ The creation of a dice Set """
    pass

class PlayDiceSet(Screen):
    """ Play a dice set"""
    pass
    
class MenuScreen(Screen):
    """ the menu screen"""
    pass

class ManagerApp(App):
    """ The app """
    title = "TextualDice"

    def build(self):
        """ add all the screen to the ScreenManager and
        lauch the post_build_init method"""        
        self.sm = ScreenManager()
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(PlayDiceSet(name='play'))
        self.sm.add_widget(CreateDiceScreen(name='createdice'))
        self.sm.add_widget(CreateDicesSetScreen(name='createdicesset'))
        self.bind(on_start=self.post_build_init)
        return self.sm

    def post_build_init(self, *args):
        """ bind the keyboard to go_menu method """
        win = Window
        win.bind(on_keyboard=self.go_menu)

    def go_menu(self, window, keycode1, keycode2, text, modifiers):
        """ executed for each key press, if the key is return then
        go to the menu screen"""
        if keycode1 in [27, 1001]:
            self.sm.current = "menu"
            return True
        return False

if __name__ == '__main__':
    ManagerApp().run()
