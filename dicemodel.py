#!/usr/bin/env python
# encoding: utf-8
"""@summary: Dice Model
@author: Vezin Aurelien A.K.A Astyan
@license: lgpl"""


import os
import sys
import random
import glob

class DiceModel(object):
    """class of a dice model
    @ivar name: name of the dice
    @type name: string
    @ivar faces: faces of the dice
    @type faces: list of string"""
    
    def __init__(self, fpath):
        """open the file and create the dice if possible
        @attention:need a test for empty file !
        @param fpath: the path of the file format
        @type fpath: string"""
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
        """roll the dice
        @return: a face of the dice
        @rtype: string
        """
        return random.choice(self.faces)
    
    def add_face(self, name):
        """add a face to the dice
        @param name: the name of the new face
        @type name: string"""
        self.faces.append(name)
    
    def del_face(self, name):
        """remove a face of the dice
        @param name: the name of the face to delete
        @type name: string"""
        self.faces.remove(name)
    
    def change_name(self, name):
        """change the name of the dice
        @param name: the new name of the dice
        @type name: string""" 
        self.name = name
    
    def save_dice(self, path = None):
        """save the dice if the dice have at least 2 faces and one name
        @param path: the path where save the dice. If None then the dice
        is saved where it was open
        @type path: string""" 
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
    """class to manage all dices
    @ivar ldices: the name and the path of each dice (name, path)
    @type ldices: (string, string)"""
    
    def __init__(self, dpath):
        """load all dices from dpath
        @param dpath: repository path where dices files are stored
        @type dpath: string"""
        self.dicespath = dpath
        self.ldices = []
        self.load(self.dicespath)
    
    def load(self, path = None):
        """add all dice store in path to the ldices list
        @param path: path to the dices, if None the path specified on
        the class instantiation will be used
        @type path: string"""
        if path == None:
            flist = glob.glob(os.path.join(self.dicespath, "*"))
        else:
            flist = glob.glob(os.path.join(path, "*"))
        for dicefile in flist:
            self.ldices.append((DiceModel(dicefile).name, dicefile))
    
    def clean(self):
        """clean the dice list"""
        self.ldices = []
    
    def get_file_from_name(self, name):
        """get the file path of a dice from a name
        @param name: the name of the dice
        @type name: string
        @return: the path to the file of the dice
        @rtype: string"""
        for (dname, dfile) in self.ldices:
            if name == dname:
                return dfile
        raise Exception("No dice named %s\n"%(name))

#to do combinaison

if __name__ == "__main__":
    #~ temporary test
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
