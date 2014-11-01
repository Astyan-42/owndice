#!/usr/bin/env python
# encoding: utf-8
"""Dice Model"""

import os
import random

class DiceModel(object):
    
    def __init__(self, fpath):
        """open the file and create the dice if possible
        need a test for empty file !"""
        self._filepath =  fpath
        self.faces = []
        self.name = ""
        dicefile = ""
        try:
            dicefile = open(fpath, "r")
        except IOError:
            return
        for line in dicefile:
            self.faces.append(line[:-1])
        self.name = self.faces[0]
        self.faces = self.faces[1:]
    
    def roll(self):
        return random.choice(self.faces)
    
    def add_face(self, name):
        self.faces.append(name)
    
    def del_face(self, name):
        self.faces.remove(name)
    
    def change_name(self, name):
        self.name = name
    
    def save_dice(self, path = None):
        if self.name == "":
            raise Exception("A dice need a name")
            exit(2)
        if len(self.faces) < 2:
            raise Exception("A dice need at least 2 faces")
            exit(3)
        if path == None:
            path = self._filepath
        try:
            dicefile = open(path , "w+")
        except IOError:
            sys.stderr.write("Error to open the file to save")
            exit(4)
        towrite = []
        towrite.append(self.name+"\n")
        for face in self.faces:
            towrite.append(face+"\n")
        dicefile.writelines(towrite)
        
    def print_dice(self):
        """temporary print no view yet"""
        print self.name, self.faces
    
    

if __name__ == "__main__":
    """temporary test"""
    print "main"
    DM = DiceModel(os.path.join(".", "dices", "six"))
    DM.print_dice()
    print DM.roll()
    DM.add_face("42")
    DM.del_face("6")
    DM.change_name("4DICE2")
    DM.print_dice()
    DM.save_dice(os.path.join(".","dices","42"))
