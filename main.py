import kivy
kivy.require('1.9.0')

import sys

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.popup import Popup
from base import *
import store

class DicePopup(Popup):
    pass

class ErrorPopup(DicePopup):
    """ Popup to show in case of erreur """

    def show_popup(self, texterror):
        """ feel the popup with the error message present in data
        @param data: dictionnary with the error type (should be 
        always 1 for this kind of popup) and the error message
        @type data: {str: int, str: str}
        """
        message = add_color(texterror, "FF0000")
        self.ids.errormessage.text = message
        self.open()

class DicesScreen(Screen):
    """ The creation of the dice """
    
    def on_pre_enter(self):
        self.dices = store.get_store("dices.pickle")
        dicesnames = [ dicename for dicename in self.dices ] + ["default"]
        self.ids.dice_model_spinner.values = dicesnames
        self.addface = DiceButton(id="addface", text="Add Face", on_release=self.add_face)
        self.delface = DiceButton(id="delface", text="Del Face", on_release=self.del_face)
        if self.ids.dice_model_spinner.text == "default":
            self.create_default()
        else:
            self.load_dice()
    
    def create_default(self):
        self.ids.inlayout.rows = self.ids.inlayout.default_rows + 1 + 1
        self.ids.dice_name.text = "default"
        self.ids.dice_color.text = "FFFFFF"
        self.faces = []
        face1label = DiceLabel(id="face1label", text="Face 1")
        face1name = DiceTextInput(id="face1name", text="Face 1")
        self.faces.append((face1label, face1name))
        self.ids.inlayout.add_widget(face1label)
        self.ids.inlayout.add_widget(face1name)
        self.ids.inlayout.add_widget(self.addface)
        self.ids.inlayout.add_widget(self.delface)
        self.ids.inlayout.height = self.ids.inlayout.nb_rows_height()        
        
    def change_dice(self):
        dices = store.get_store("dices.pickle")
        #delete everything that belong to the other dice
        self.ids.inlayout.remove_widget(self.addface)
        self.ids.inlayout.remove_widget(self.delface)
        for flabel, fname in self.faces:
            self.ids.inlayout.remove_widget(flabel)
            self.ids.inlayout.remove_widget(fname)
        self.faces = []
        #set the number of rows
        if self.ids.dice_model_spinner.text == "default":
            self.create_default()
        else:
            self.load_dice()
    
    def load_dice(self): 
        self.ids.inlayout.rows = self.ids.inlayout.default_rows + 1 + len(self.dices[self.ids.dice_model_spinner.text]["data"]["faces"])
        self.ids.dice_name.text = self.ids.dice_model_spinner.text
        self.ids.dice_color.text = self.dices[self.ids.dice_model_spinner.text]["data"]["color"]
        #create the faces
        for i in range(0, len(self.dices[self.ids.dice_model_spinner.text]["data"]["faces"])):
            labelid = "face" + str(i+1) +"label"
            labeltext = "Face "+str(i+1)
            nameid = "face" + str(i+1) +"name"
            nametext = self.dices[self.ids.dice_model_spinner.text]["data"]["faces"][i]
            facelabel = DiceLabel(id=labelid, text=labeltext)
            facename = DiceTextInput(id=nameid, text=nametext)
            self.faces.append((facelabel, facename))
            self.ids.inlayout.add_widget(facelabel)
            self.ids.inlayout.add_widget(facename)
        self.ids.inlayout.add_widget(self.addface)
        self.ids.inlayout.add_widget(self.delface)
        self.ids.inlayout.height = self.ids.inlayout.nb_rows_height()
    
    def add_face(self, buttoninstance):
        self.ids.inlayout.remove_widget(self.addface)
        self.ids.inlayout.remove_widget(self.delface)
        facenb = len(self.faces)
        labelid = "face" + str(facenb+1) +"label"
        labeltext = "Face "+ str(facenb+1)
        nameid = "face" + str(facenb+1) +"name"
        nametext = "Face "+ str(facenb+1)
        facelabel = DiceLabel(id=labelid, text=labeltext)
        facename = DiceTextInput(id=nameid, text=nametext)
        self.ids.inlayout.add_widget(facelabel)
        self.ids.inlayout.add_widget(facename)
        self.faces.append((facelabel, facename))
        self.ids.inlayout.rows = self.ids.inlayout.default_rows + 1 + len(self.faces)
        self.ids.inlayout.add_widget(self.addface)
        self.ids.inlayout.add_widget(self.delface)
        self.ids.inlayout.height = self.ids.inlayout.nb_rows_height()
        
    def del_face(self, buttoninstance):
        if len(self.faces) != 0:
            (labelw, namew) = self.faces[-1]
            self.ids.inlayout.remove_widget(labelw)
            self.ids.inlayout.remove_widget(namew)
            self.faces = self.faces[0:len(self.faces)-1]
            self.ids.inlayout.rows = self.ids.inlayout.default_rows + 1 + len(self.faces)
            self.ids.inlayout.height = self.ids.inlayout.nb_rows_height()
                
    def execute(self):
        if self.ids.action.text == "Add":
            self.new_dice()
        elif self.ids.action.text == "Edit":
            self.edit_dice()
        elif self.ids.action.text == "Delete":
            self.del_dice()
    
    def create_error_popup(self):
        t, v, tb = sys.exc_info()
        self._popup = ErrorPopup()
        self._popup.show_popup(str(v))
        
    def edit_dice(self):
        data = {"faces" : [], "color" : self.ids.dice_color.text}
        for (facelabel, facename) in self.faces:
            data["faces"].append(facename.text)
        try:
            store.edit_data("dices.pickle", self.ids.dice_name.text, data)
        except store.StoreException:
            self.create_error_popup()
    
    def new_dice(self):
        data = {"faces" : [], "color" : self.ids.dice_color.text}
        for (facelabel, facename) in self.faces:
            data["faces"].append(facename.text)
        try:
            store.add_data("dices.pickle", self.ids.dice_name.text, data)
        except store.StoreException:
            self.create_error_popup()
        dices = store.get_store("dices.pickle")
        dicesnames = [ dicename for dicename in dices ] + ["default"]
        self.ids.dice_model_spinner.values = dicesnames
        
    def del_dice(self):
        try:
            store.del_data("dices.pickle", self.ids.dice_name.text)
        except store.StoreException:
            self.create_error_popup()
        dices = store.get_store("dices.pickle")
        dicesnames = [ dicename for dicename in dices ] + ["default"]
        self.ids.dice_model_spinner.values = dicesnames
        
    def on_leave(self):
        self.ids.inlayout.remove_widget(self.addface)
        self.ids.inlayout.remove_widget(self.delface)
        for w1, w2 in self.faces:
            self.ids.inlayout.remove_widget(w1)
            self.ids.inlayout.remove_widget(w2)

        
class DicesSetsScreen(Screen):
    """ The creation of a dice Set """
    
    def on_pre_enter(self):
        dices = store.get_store("dices.pickle")
        self.dicesnames = [ dicename for dicename in dices ] + ["default"]
        self.dicessets = store.get_store("dicessets.pickle")
        dicessetsnames = [ dicesetname for dicesetname in self.dicessets ] + ["default"]
        self.ids.diceset_model_spinner.values = dicessetsnames
        self.adddice = DiceButton(id="adddice", text="Add Dice", on_release=self.add_dice)
        self.deldice = DiceButton(id="deldice", text="Del Dice", on_release=self.del_dice)
        if self.ids.diceset_model_spinner.text == "default":
            self.create_default()
        else:
            self.load_diceset()
    
    def create_default(self):
        self.ids.inlayout.rows = self.ids.inlayout.default_rows + 1 + 1
        self.ids.diceset_name.text = "default"
        #add dice spinner
        self.dices = []
        dicelabel = DiceLabel(id="dice1label", text="Dice 1")
        dicename = DiceSpinner(id="dice1name", text="default", values=self.dicesnames)
        self.dices.append((dicelabel, dicename))
        self.ids.inlayout.add_widget(dicelabel)
        self.ids.inlayout.add_widget(dicename)
        #add buttons
        self.ids.inlayout.add_widget(self.adddice)
        self.ids.inlayout.add_widget(self.deldice)
        self.ids.inlayout.height = self.ids.inlayout.nb_rows_height() 
    
    def change_diceset(self):
        pass
    
    def load_diceset(self):
        pass
    
    def add_dice(self, buttoninstance):
        self.ids.inlayout.remove_widget(self.adddice)
        self.ids.inlayout.remove_widget(self.deldice)
        dicenb = len(self.dices)
        diceid = "dice" + str(dicenb+1) +"label"
        labeltext = "Dice "+ str(dicenb+1)
        listid = "dice" + str(dicenb+1) +"name"
        listdice = self.dicesnames
        listtext = "default"
        dicelabel = DiceLabel(id=diceid, text=labeltext)
        dicename = DiceSpinner(id=listid, text=listtext, values=listdice)
        self.ids.inlayout.add_widget(dicelabel)
        self.ids.inlayout.add_widget(dicename)
        self.dices.append((dicelabel, dicename))
        self.ids.inlayout.rows = self.ids.inlayout.default_rows + 1 + len(self.dices)
        self.ids.inlayout.add_widget(self.adddice)
        self.ids.inlayout.add_widget(self.deldice)
        self.ids.inlayout.height = self.ids.inlayout.nb_rows_height()
    
    def del_dice(self, buttoninstance):
        if len(self.dices) != 0:
            (labelw, namew) = self.dices[-1]
            self.ids.inlayout.remove_widget(labelw)
            self.ids.inlayout.remove_widget(namew)
            self.dices = self.dices[0:len(self.dices)-1]
            self.ids.inlayout.rows = self.ids.inlayout.default_rows + 1 + len(self.dices)
            self.ids.inlayout.height = self.ids.inlayout.nb_rows_height()
        
    def execute(self):
        try:
            if self.ids.action.text == "Add":
                self.new_diceset()
            elif self.ids.action.text == "Edit":
                self.edit_diceset()
            elif self.ids.action.text == "Delete":
                self.del_diceset()
        except store.StoreException:
            self.create_error_popup()
    
    def create_error_popup(self):
        t, v, tb = sys.exc_info()
        self._popup = ErrorPopup()
        self._popup.show_popup(str(v))
    
    def new_diceset(self):
        data = {"dices" : []}
        if len(self.dices) == 0:
            raise store.StoreException("Cannot create an empty diceset")
        for (dicelabel, dicename) in self.dices:
            data["dices"].append(dicename.text)
            if dicename.text == "default":
                raise store.StoreException("Cannot use default dice in a diceset")
        try:
            store.add_data("dicessets.pickle", self.ids.diceset_name.text, data)
        except store.StoreException:
            self.create_error_popup()
        dicessets = store.get_store("dicessets.pickle")
        dicessetsnames = [ dicesetname for dicesetname in dicessets ] + ["default"]
        self.ids.diceset_model_spinner.values = dicessetsnames
        
    def edit_diceset(self):
        data = {"dices" : []}
        if len(self.dices) == 0:
            raise store.StoreException("Cannot save an empty diceset")
        for (dicelabel, dicename) in self.dices:
            data["dices"].append(dicename.text)
            if dicename.text == "default":
                raise store.StoreException("Cannot use default dice in a diceset")
        try:
            store.del_data("dicessets.pickle", self.ids.diceset_name.text, data)
        except store.StoreException:
            self.create_error_popup()
    
    def del_diceset(self):
        try:
            store.del_data("dicessets.pickle", self.ids.diceset_name.text)
        except store.StoreException:
            self.create_error_popup()
        dicessets = store.get_store("dicessets.pickle")
        dicessetsnames = [ dicesetname for dicesetname in dicessets ] + ["default"]
        self.ids.dice_model_spinner.values = dicesnames
        
    def on_leave(self):
        self.ids.inlayout.remove_widget(self.adddice)
        self.ids.inlayout.remove_widget(self.deldice)
        for w1, w2 in self.dices:
            self.ids.inlayout.remove_widget(w1)
            self.ids.inlayout.remove_widget(w2)

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
