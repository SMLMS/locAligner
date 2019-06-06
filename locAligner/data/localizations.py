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
# =============================================================================
#         self._dx = dx
#         self._dy = dy
#         
#     @property
#     def dx(self):
#         return self._dx
# 
#     @dx.setter
#     def dx(self, value):
#         self._dx = value
#         
#     @property
#     def dy(self):
#         return self._dx
# 
#     @dy.setter
#     def dx(self, value):
#         self._dx = value
# =============================================================================
            
    def clusterLocalizations(self, eps= 30.0, min_samples = 5):
        cluster= DBSCAN(algorithm='auto',
                        eps=eps,
                        leaf_size=30,
                        metric='euclidean',
                        metric_params=None,
                        min_samples=min_samples,
                        n_jobs=-1,
                        p=None).fit(self._dataFrame[[self._coordianteNames[0],self._coordianteNames[1]]].values)
        self._dataFrame = self._dataFrame.assign(cluster = cluster.labels_)
        
    def clusterArray(self):
        return set(self._dataFrame['cluster'].values)
        
    def plotLocalizations(self):
        ax2 = self._dataFrame.plot.scatter(x = self._coordianteNames[0],
                                           y = self._coordianteNames[1],
                                           c = 'cluster',
                                           colormap='viridis')
    
    def plotCluster(self, cNum = 0):
        self._dataFrame[self._dataFrame['cluster'] == cNum].plot.scatter(x = self._coordianteNames[0],
                       y = self._coordianteNames[1],
                       c = 'frame',
                       colormap='rainbow')
    
def main():
    dataSet = SMLM_localizations()
    dataSet.browseFile()
    dataSet.updateNames()
    print(dataSet.fileName)
    print(dataSet.baseName)
    print(dataSet.folderName)
    
    
if __name__ == '__main__':
    main()