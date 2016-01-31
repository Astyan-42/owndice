import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.popup import Popup
from base import *
import store


class DicesScreen(Screen):
    """ The creation of the dice """
    
    def on_pre_enter(self):
        dices = store.get_store("dices.pickle")
        dicesnames = ["default"] + [ dicename for dicename in dices ]
        self.ids.dice_model_spinner.values = dicesnames
        self.faces = []
        face1label = DiceLabel(id="face1label", text="Face 1")
        face1name = DiceTextInput(id="face1name", text="Face 1")
        self.faces.append((face1label, face1name))
        self.ids.inlayout.add_widget(face1label)
        self.ids.inlayout.add_widget(face1name)
        self.addface = DiceButton(id="addface", text="Add Face", on_release=self.add_face)
        self.delface = DiceButton(id="delface", text="Del Face", on_release=self.del_face)
        self.ids.inlayout.add_widget(self.addface)
        self.ids.inlayout.add_widget(self.delface)
        self.ids.inlayout.height = self.ids.inlayout.nb_rows_height()
        
        
        #~ self.ids.dice_model_spinner.text = "default"
        
    def change_dice(self):
        dices = store.get_store("dices.pickle")
        self.ids.dice_name.text = self.ids.dice_model_spinner.text
        self.ids.dice_color.text = dices[self.ids.dice_model_spinner.text]["data"]["color"]
        #delete everything that belong to the other dice
        self.ids.inlayout.remove_widget(self.addface)
        self.ids.inlayout.remove_widget(self.delface)
        for flabel, fname in self.faces:
            self.ids.inlayout.remove_widget(flabel)
            self.ids.inlayout.remove_widget(fname)
        self.faces = []
        #set the number of rows
        self.ids.inlayout.rows = self.ids.inlayout.default_rows + 1 + len(dices[self.ids.dice_model_spinner.text]["data"]["faces"])
        #create the faces
        for i in range(0, len(dices[self.ids.dice_model_spinner.text]["data"]["faces"])):
            labelid = "face" + str(i+1) +"label"
            labeltext = "Face "+str(i+1)
            nameid = "face" + str(i+1) +"name"
            nametext = dices[self.ids.dice_model_spinner.text]["data"]["faces"][i]
            facelabel = DiceLabel(id=labelid, text=labeltext)
            facename = DiceTextInput(id=nameid, text=nametext)
            self.faces.append((facelabel, facename))
            self.ids.inlayout.add_widget(facelabel)
            self.ids.inlayout.add_widget(facename)
        self.ids.inlayout.add_widget(self.addface)
        self.ids.inlayout.add_widget(self.delface)
        self.ids.inlayout.height = self.ids.inlayout.nb_rows_height()
    
    def add_face(self, buttoninstance):
        pass
    
    def del_face(self, buttoninstance):
        pass
    
    def edit_dice(self):
        pass
    
    def new_dice(self):
        pass
        
    def del_dice(self):
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
