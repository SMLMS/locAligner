# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 11:33:08 2019

@author: malkusch
"""

import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename
import csv
import os
from shutil import copyfile
import h5py
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
        locs = self._dataFrame[[self._coordianteNames[0], self._coordianteNames[1]]].values
        p=np.zeros([3,1])
        p[2]=1
        for i in range (0,self._dataFrame.shape[0]):
            p[0]=locs[i,0]
            p[1]=locs[i,1]
            o=np.dot(self._affineMatrix,p)
            locs[i,0]=o[0]
            locs[i,1]=o[1]
        self._dataFrame = self._dataFrame.assign(**{self._coordianteNames[0]: locs[:,0]}).round(1)
        self._dataFrame = self._dataFrame.assign(**{self._coordianteNames[1]: locs[:,1]}).round(1)
        
    def saveDataFrame(self, prefix='registered'):
        if (self._fileName):
            filename, file_extension = os.path.splitext(self._fileName)
            if(file_extension == ".csv"):
                self.saveDataFrameCsv()
            elif((file_extension == ".hdf5") or (file_extension == ".h5")):
                self.saveDataFrameHdf5()
            else:
                print("file of type "+file_extension+" is not understood")
        else:
            print('No file name selected!')
    
    def saveDataFrameCsv(self, prefix='registered'):
        outName = str('%s\%s_%s%s' %(self._folderName, self._baseName, prefix, '.csv'))
        self._dataFrame.to_csv(path_or_buf = outName, index=False, quoting=csv.QUOTE_NONNUMERIC)
        print("Registered dataset written to: %s" % (outName))
        
    def saveDataFrameHdf5(self,prefix='registered', pxlSize=160.0):
        outName = str('%s\%s_%s%s' %(self._folderName, self._baseName[:-1], prefix, '.hdf5'))
        copyfile(self._fileName, outName)
        f = h5py.File(outName, 'r+')     # open the file
        data = f['locs']       # load the data
        data['x'] = self._dataFrame[self._coordianteNames[0]].values/pxlSize
        data['y'] = self._dataFrame[self._coordianteNames[1]].values/pxlSize
        f.close()

        
