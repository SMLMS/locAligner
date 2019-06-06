# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 13:05:50 2019

@author: malkusch
"""
from ..jupyter import laWidgets

class LaTransformWidgets(laWidgets.LaWidgets):
    def __init__(self):
        laWidgets.LaWidgets.__init__(self)
        self.loadDataButton = self.createButton(desc = 'load Dataset')
        self.pxlSize = self.createTextFloat(val=160.0, minVal=0.0, maxVal=200.0, stepSize=0.1, desc="pixleSize [nm]")
        self.loadMatrixButton = self.createButton(desc = 'load Matrix')
        self.outFilePrefix = self.createTextStr(value='registered', desc='file prefix', placeHolder = 'registered')
        self.transformButton = self.createButton(desc = 'transform')