# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 13:03:32 2019

@author: malkusch
"""

#import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull
from ..data import dataObject

class SMLM_fiducials(dataObject.SMLM_dataObject):
    def __init__(self, dx = 0.0, dy=0.0):
        dataObject.SMLM_dataObject.__init__(self)
        self._dx = dx
        self._dy = dy
        
    @property
    def dx(self):
        return self._dx

    @dx.setter
    def dx(self, value):
        self._dx = value
        
    @property
    def dy(self):
        return self._dx

    @dy.setter
    def dx(self, value):
        self._dx = value
            
    def createClusterDataSet(self, clDataFrame = pd.DataFrame()):
        emptyArray =[0.0] * (len(set(clDataFrame['cluster'].values)))        
        self._dataFrame = pd.DataFrame ({'cl_idx': emptyArray,
                                         'x_mean': emptyArray,
                                         'x_std': emptyArray,
                                         'y_mean': emptyArray,
                                         'y_std': emptyArray,
                                         'intensity': emptyArray,
                                         'area': emptyArray})
        tempDataFrame = pd.DataFrame()
        for  i in list(set(clDataFrame['cluster'].values))[:-1]:
            tempDataFrame = clDataFrame.loc[clDataFrame['cluster'] == i]
            self._dataFrame.at[i, 'cl_idx'] = i
            self._dataFrame.at[i, 'x_mean'] = tempDataFrame["x [nm]"].mean()
            self._dataFrame.at[i, 'x_std'] = tempDataFrame["x [nm]"].std()
            self._dataFrame.at[i, 'y_mean'] = tempDataFrame["y [nm]"].mean()
            self._dataFrame.at[i, 'y_std'] = tempDataFrame["y [nm]"].std()
            self._dataFrame.at[i, 'intensity'] = tempDataFrame.shape[0]
            self._dataFrame.at[i, 'area'] = ConvexHull(tempDataFrame[["x [nm]" , "y [nm]" ]].values).area

    def plotFiducials(self):
        self._dataFrame.plot.scatter(x = 'x_mean',
                                     y= 'y_mean',
                                     c = 'cl_idx',
                                     colormap='viridis')