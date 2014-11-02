#!/usr/bin/env python
# encoding: utf-8
"""Dice Model"""

import os
import sys
import random
import glob

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
        if len(self.faces) < 2:
            raise Exception("A dice need at least 2 faces")
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
    
class AllDices(object):
    
    def __init__(self, dpath):
        self.dicespath = dpath
        self.ldices = []
        self.load(self.dicespath)
    
    def load(self, path = None):
        if path == None:
            flist = glob.glob(os.path.join(self.dicespath, "*"))
        else:
            flist = glob.glob(os.path.join(path, "*"))
        for dicefile in flist:
            self.ldices.append((DiceModel(dicefile).name, dicefile))
    
    def clean(self):
        self.ldices = []
    
    def get_file_from_name(self, name):
        for (dname, dfile) in self.ldices:
            if name == dname:
                return dfile
        raise Exception("No dice named %s\n"%(name))

#to do combinaison

if __name__ == "__main__":
    """temporary test"""
    print "main"
    AD = AllDices(os.path.join(".", "dices"))
    print AD.get_file_from_name("SIX")
    #~ print AD.rolls(["SIX", "lose"])
    #~ DM = DiceModel(os.path.join(".", "dices", "six"))
    #~ DM.print_dice()
    #~ print DM.roll()
    #~ DM.add_face("42")
    #~ DM.del_face("6")
    #~ DM.change_name("4DICE2")
    #~ DM.print_dice()
    #~ DM.save_dice(os.path.join(".","dices","42"))
