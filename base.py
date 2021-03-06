
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.metrics import sp
from kivy.lang import Builder
Builder.load_file('base.kv')

def add_color(text, color):
    return "[color="+color+"]"+text+"[/color]" 

class DiceButton(Button):
    pass
  
class DiceLabel(Label):
    pass

class DiceTextInput(TextInput):
    pass

class DiceSpinner(Spinner):
    pass
    
class ScrollViewSpe(ScrollView):
    """ Special class made to give it's own value at his layout child
    See the kv file for an exemple of use """

    def change_child_width(self, wid):
        for child in self.children:
            child.change_width(wid)
        return wid

class DiceLayout(GridLayout):
    """Special Layout use to choose the minimal size allowed
    if the actual size of the parent widget is lower.
    If the actual size of the parent is biger then get the biger size.
    /!\ The parent must be a ScrollViewSpe
    """
    
    def nb_rows_height(self):
        return 75 * self.rows + 10
    
    def set_min_width(self):
        self.minimum_width = sp(350)
    
    def change_width(self, wid):
        #~ reset because of a bug in kivy
        self.set_min_width()
        
        if wid > self.minimum_width:
            self.width = wid
        else:
            self.width = self.minimum_width


class TopScreenLayout(DiceLayout):
    """ set the size of the layout from minimals values and the size
    of the scrollviewspe parrent."""
    
    def set_min_height(self):
        self.minimum_height = sp(100) * self.rows + sp(10)
        
    def set_min_width(self):
        self.minimum_width = sp(290)

class TopPopupLayout(DiceLayout):
    """ set the size of the layout from minimals values and the size
    of the scrollviewspe parrent."""
    def set_min_height(self):
        self.minimum_height = sp(75) * self.rows + sp(20)

    def set_min_width(self):
        self.minimum_width = sp(200)


