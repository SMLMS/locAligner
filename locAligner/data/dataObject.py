# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 15:37:29 2019

@author: malkusch
"""
import os
import tkinter as tk
from tkinter.filedialog import askopenfilename
import numpy as np
import pandas as pd
import h5py

class SMLM_dataObject:
    def __init__(self, fileName = ""):
        self._fileName = fileName
        self._baseName = ""
        self._folderName = ""
        self._dataFrame = pd.DataFrame()
        self._coordianteNames = ['x [nm]', 'y [nm]']
        
    @property
    def fileName(self):
        print("returning fileName")
        return self._fileName
    
    @fileName.setter
    def fileName(self, value):
        print("set fileName")
        self._fileName = value
        
    @property
    def baseName(self):
        print("return baseName")
        return self._baseName
    
    @property
    def folderName(self):
        print("return folderName")
        return self._folderName
    
    @property
    def dataFrame(self):
        return self._dataFrame
    
    @property
    def coordinateNames(self):
        return self._coordianteNames
    
    @coordinateNames.setter
    def coordinateNames(self, value):
        self._coordianteNames = value
    
    def updateNames(self):
        if (len(self._fileName)>0):
            self._folderName = os.path.dirname(self._fileName)
            self._baseName = os.path.basename(self._fileName)[:-4]
        else:
            print("No fileName selected!")
    
    def browseFile(self):
        root = tk.Tk()
        root.withdraw()
        root.update()
        root.name = askopenfilename(title="import thunderSTORM localization file", filetypes=(("comma separated files", "*.csv"),
                                                                                              ("HDF5 files", "*.hdf5"),
                                                                                              ("HDF5 files", "*.h5"),
                                                                                              ("All files", "*.*") ))
        self._fileName = root.name
        root.update()
        root.destroy()
        
    def importData(self, pxlSize=160.0):
        if (self._fileName):
            filename, file_extension = os.path.splitext(self._fileName)
            if(file_extension == ".csv"):
                self.importDataFromCsv()
            elif((file_extension == ".hdf5") or (file_extension == ".h5")):
                self.importDataFromHdf5(pxlSize)
            else:
                print("file of type "+file_extension+" is not understood")
        else:
            print('No file name selected!')
        
    def importDataFromCsv(self):
        self._dataFrame = pd.read_csv(self._fileName)
        for entry in list(self._dataFrame.columns.values):
            if entry == 'x [px]':
                print('Error: spatial units need to be of type [nm]')
                break
            
    def importDataFromHdf5(self, pxlSize = 160.0):
        #self._dataFrame = pd.read_hdf(self._fileName)
        self._coordianteNames = ['x [nm]','y [nm]']
        f = h5py.File(self._fileName, 'r')
        locs=np.zeros([len(f['locs']['x'][:]),2])
        locs[:,0] = f['locs']['x'][:]*pxlSize
        locs[:,1] = f['locs']['y'][:]*pxlSize
        #self._dataFrame = pd.DataFrame(locs, index=np.arange(0,len(locs)), columns=('x [px]', 'y [px]'))
        self._dataFrame = pd.DataFrame(locs, index=np.arange(0,len(locs)), columns=(self._coordianteNames[0], self._coordianteNames[1]))
        f.close()
    
    def viewData(self):
        print(self._dataFrame.head())
        
def main():
    data = SMLM_dataObject()
    data.browseFile()
    data.updateNames()
    print(data.fileName)
    print(data.baseName)
    print(data.folderName)
    
    
if __name__ == '__main__':
    main()