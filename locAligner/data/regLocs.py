# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 11:33:08 2019

@author: malkusch
"""

import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename
import csv
from ..data import localizations

class SMLM_regLocs(localizations.SMLM_localizations):
    def __init__(self):
        localizations.SMLM_localizations.__init__(self)
        self._affineMatrix = np.zeros([3,3],float)
        
    def loadMatrix(self):
        root = tk.Tk()
        root.withdraw()
        root.update()
        root.name = askopenfilename(title="import affine trnasformation matrix", filetypes=(("comma separated files", "*matrix.csv"),
                                       ("All files", "*.*") ))
        fileName = root.name
        root.update()
        root.destroy()
        self._affineMatrix= np.loadtxt(fileName, dtype=float, comments='#', delimiter=',')
        print("Matrix loaded from: %s" % (fileName))
        
    def affineTransformation(self):
        locs = self._dataFrame[['x [nm]', 'y [nm]']].values
        p=np.zeros([3,1])
        p[2]=1
        for i in range (0,self._dataFrame.shape[0]):
            p[0]=locs[i,0]
            p[1]=locs[i,1]
            o=np.dot(self._affineMatrix,p)
            locs[i,0]=o[0]
            locs[i,1]=o[1]
        self._dataFrame = self._dataFrame.assign(**{'x [nm]': locs[:,0]}).round(1)
        self._dataFrame = self._dataFrame.assign(**{'y [nm]': locs[:,1]}).round(1)
        
    def saveDataFrame(self, prefix='registered'):
        outName = str('%s\%s_%s%s' %(self._folderName, self._baseName, prefix, '.txt'))
        self._dataFrame.to_csv(path_or_buf = outName, index=False, quoting=csv.QUOTE_NONNUMERIC)
        print("Registered dataset written to: %s" % (outName))
