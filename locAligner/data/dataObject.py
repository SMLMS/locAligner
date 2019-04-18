# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 15:37:29 2019

@author: malkusch
"""
import os
import tkinter as tk
from tkinter.filedialog import askopenfilename
import pandas as pd

class SMLM_dataObject:
    def __init__(self, fileName = ""):
        self._fileName = fileName
        self._baseName = ""
        self._folderName = ""
        self._dataFrame = pd.DataFrame()
        
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
                                       ("All files", "*.*") ))
        self._fileName = root.name
        root.update()
        root.destroy()
        
    def importData(self):
        if (self._fileName):
            self._dataFrame = pd.read_csv(self._fileName)
        else:
            print('No file name selected!')
    
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