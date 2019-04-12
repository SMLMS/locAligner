# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 15:28:36 2019

@author: malkusch
"""
#import numpy as np
from sklearn.cluster import DBSCAN
from ..data import dataObject

class SMLM_localizations(dataObject.SMLM_dataObject):
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
            
    def clusterLocalizations(self):
        cluster= DBSCAN(algorithm='auto',
                        eps=30,
                        leaf_size=30,
                        metric='euclidean',
                        metric_params=None,
                        min_samples=5,
                        n_jobs=-1,
                        p=None).fit(self._dataFrame[['x [nm]','y [nm]']].values)
        self._dataFrame = self._dataFrame.assign(cluster = cluster.labels_)
        
    def plotLocalizations(self):
        ax2 = self._dataFrame.plot.scatter(x='x [nm]',
                                          y = 'y [nm]',
                                          c = 'cluster',
                                          colormap='viridis')
    
    def plotCluster(self, cNum = 0):
        self._dataFrame[self._dataFrame['cluster'] == cNum].plot.scatter(x='x [nm]', y='y [nm]')
    
def main():
    dataSet = SMLM_localizations()
    dataSet.browseFile()
    dataSet.updateNames()
    print(dataSet.fileName)
    print(dataSet.baseName)
    print(dataSet.folderName)
    
    
if __name__ == '__main__':
    main()