import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.popup import Popup


class DicesScreen(Screen):
    """ The creation of the dice """
    pass
    
class DicesSetsScreen(Screen):
    """ The creation of a dice Set """
    pass

class PlayDiceSet(Screen):
    """ Play a dice set"""
    pass

class DicesSetResultPopup(Popup):
    """ show a DiceSetResult """
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
        self.sm.add_widget(DicesScreen(name='dices'))
        self.sm.add_widget(DicesSetsScreen(name='dicessets'))
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
