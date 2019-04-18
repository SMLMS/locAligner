# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 13:03:32 2019

@author: malkusch
"""

import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull
from sklearn.neighbors import NearestNeighbors
from ..data import dataObject

class SMLM_fiducials(dataObject.SMLM_dataObject):
    def __init__(self, dx_value = 0.0, dy_value=0.0):
        dataObject.SMLM_dataObject.__init__(self)
        self._filteredDataFrame = pd.DataFrame()
        self._translatedDataFrame = pd.DataFrame()
        self._fiducialDataFrame = pd.DataFrame()
        self._affineMatrix = np.zeros([3,3],float)
        self._dx = dx_value
        self._dy = dy_value
        
    @property
    def dx(self):
        return self._dx

    @dx.setter
    def dx(self, value):
        self._dx = value
        
    @property
    def dy(self):
        return self._dy

    @dy.setter
    def dy(self, value):
        self._dy = value
            
# =============================================================================
#     def createClusterDataSet(self, clDataFrame = pd.DataFrame()):
#         emptyArray =[0.0] * (len(set(clDataFrame['cluster'].values)))        
#         self._dataFrame = pd.DataFrame ({'cl_idx': emptyArray,
#                                          'x_mean': emptyArray,
#                                          'x_std': emptyArray,
#                                          'y_mean': emptyArray,
#                                          'y_std': emptyArray,
#                                          'intensity': emptyArray,
#                                          'area': emptyArray})
#         tempDataFrame = pd.DataFrame()
#         for  i in list(set(clDataFrame['cluster'].values))[:-1]:
#             tempDataFrame = clDataFrame.loc[clDataFrame['cluster'] == i]
#             self._dataFrame.at[i, 'cl_idx'] = i
#             self._dataFrame.at[i, 'x_mean'] = tempDataFrame["x [nm]"].mean()
#             self._dataFrame.at[i, 'x_std'] = tempDataFrame["x [nm]"].std()
#             self._dataFrame.at[i, 'y_mean'] = tempDataFrame["y [nm]"].mean()
#             self._dataFrame.at[i, 'y_std'] = tempDataFrame["y [nm]"].std()
#             self._dataFrame.at[i, 'intensity'] = tempDataFrame.shape[0]
#             self._dataFrame.at[i, 'area'] = ConvexHull(tempDataFrame[["x [nm]" , "y [nm]" ]].values).area
#             
# =============================================================================
    def initFiducalDataSet(self, clDataFrame = pd.DataFrame()):
        emptyArray =[0.0] * (len(set(clDataFrame['cluster'].values))-1)
        tempDataFrame = pd.DataFrame ({'cl_idx': emptyArray,
                                         'x_mean': emptyArray,
                                         'x_std': emptyArray,
                                         'y_mean': emptyArray,
                                         'y_std': emptyArray,
                                         'intensity': emptyArray,
                                         'area': emptyArray,
                                         'channel': emptyArray},)
        return tempDataFrame
    
    def createClusterDataSet(self, clDataFrame = pd.DataFrame(), channel = 1):
        clusterDataFrame = self.initFiducalDataSet(clDataFrame)
        for  i in list(set(clDataFrame['cluster'].values))[:-1]:
            tempDataFrame = clDataFrame.loc[clDataFrame['cluster'] == i]
            clusterDataFrame.at[i, 'cl_idx'] = i
            clusterDataFrame.at[i, 'x_mean'] = tempDataFrame["x [nm]"].mean()
            clusterDataFrame.at[i, 'x_std'] = tempDataFrame["x [nm]"].std()
            clusterDataFrame.at[i, 'y_mean'] = tempDataFrame["y [nm]"].mean()
            clusterDataFrame.at[i, 'y_std'] = tempDataFrame["y [nm]"].std()
            clusterDataFrame.at[i, 'intensity'] = tempDataFrame.shape[0]
            clusterDataFrame.at[i, 'area'] = ConvexHull(tempDataFrame[["x [nm]" , "y [nm]" ]].values).area
            clusterDataFrame.at[i, 'channel'] = channel
        return clusterDataFrame
            
    def createFiducialDataSet(self, clDataFrame1 = pd.DataFrame(), clDataFrame2 = pd.DataFrame()):
        self._dataFrame = pd.concat([self.createClusterDataSet(clDataFrame1,1),
                                     self.createClusterDataSet(clDataFrame2,2)])
        self._filteredDataFrame = self._dataFrame.copy()
        self._translatedDataFrame = self._dataFrame.copy()
        
    def filterDataFrame(self,
                        minX=0, maxX=1,
                        minStdX=0 , maxStdX=1 ,
                        minY=0, maxY=1,
                        minStdY=0,maxStdY=1,
                        minInt=0, maxInt=1,
                        minArea=0, maxArea=1):
        idx1 = self._dataFrame['x_mean'] >= minX
        idx2 = self._dataFrame['x_mean'] <= maxX
        idx3 = self._dataFrame['x_std'] >= minStdX
        idx4 = self._dataFrame['x_std'] <= maxStdX
        idx5 = self._dataFrame['y_mean'] >= minY
        idx6 = self._dataFrame['y_mean'] <= maxY
        idx7 = self._dataFrame['y_std'] >= minStdY
        idx8 = self._dataFrame['y_std'] <= maxStdY
        idx9 = self._dataFrame['intensity'] >= minInt
        idx10 = self._dataFrame['intensity'] <= maxInt
        idx11 = self._dataFrame['area'] >= minArea
        idx12 = self._dataFrame['area'] <= maxArea
        self._filteredDataFrame = self._dataFrame[idx1 &
                                                  idx2 &
                                                  idx3 &
                                                  idx4 &
                                                  idx5 &
                                                  idx6 &
                                                  idx7 &
                                                  idx8 &
                                                  idx9 &
                                                  idx10 &
                                                  idx11 &
                                                  idx12] 
        
    def trnaslateChannel2(self):
        tempDataFrame1 = self._filteredDataFrame[self._filteredDataFrame['channel'] == 1]
        tempDataFrame2 = self._filteredDataFrame[self._filteredDataFrame['channel'] == 2]
        tempDataFrame2 = tempDataFrame2.assign(x_mean = tempDataFrame2['x_mean'].add(self._dx))
        tempDataFrame2 = tempDataFrame2.assign(y_mean = tempDataFrame2['y_mean'].add(self._dy))
        self._translatedDataFrame = pd.concat([tempDataFrame1, tempDataFrame2])
        
        
    def plotFiducials(self):
        self._translatedDataFrame.plot.scatter(x = 'x_mean',
                                     y= 'y_mean',
                                     c = 'channel',
                                     colormap='viridis')
        
    def sortFiducials(self, thresholdDistance = 250):
        nbrModel = NearestNeighbors(n_neighbors=1, algorithm='auto')
        channel1 = self._translatedDataFrame[self._translatedDataFrame['channel'] == 1]
        channel2 = self._translatedDataFrame[self._translatedDataFrame['channel'] == 2]
        nbrs= nbrModel.fit(channel2[['x_mean', 'y_mean']].values)
        distances, indices = nbrs.kneighbors(channel1[['x_mean', 'y_mean']].values)
        channel1 = channel1.assign(nn_idx= indices[:])
        channel1 = channel1.assign(nn_dist= distances[:])
        channel1 = channel1.sort_values(by=['nn_dist'])
        channel1.plot(y='nn_dist', use_index=False)
        channel1 = channel1[channel1['nn_dist'] <= thresholdDistance]
        channel2 = self._filteredDataFrame[self._filteredDataFrame['channel'] == 2]
        channel2 = channel2.reindex(channel1['nn_idx'].values)
        self._fiducialDataFrame = pd.concat([channel1.loc[:,:'channel'], channel2])
        
    def createAffineMatrix(self):
        '''
        Receives two fiducial localization lists from corresponding channels. Creates affine transformation matrix by least square fitting. returns matrix.
        '''
        beadNumber=self._fiducialDataFrame['channel'].value_counts()
        if (beadNumber.values[0] != beadNumber.values[1]):
            print('fiducial data set has wrong dimensions\nchannel1: %i\nchannel2: %i' % (beadNumber.values[0], beadNumber.values[1]))
            return False
        tp = self._fiducialDataFrame[self._fiducialDataFrame['channel']==1][['x_mean', 'y_mean']].values
        fp = self._fiducialDataFrame[self._fiducialDataFrame['channel']==2][['x_mean', 'y_mean']].values
        n = beadNumber.values[0]
        m=np.zeros ([2*n,6], float)
        m[0:n,0]=fp[:,0]
        m[0:n,1]=fp[:,1]
        m[0:n,2]=1
        m[n:2*n,3]=fp[:,0]
        m[n:2*n,4]=fp[:,1]
        m[n:2*n,5]=1
        b=np.zeros([2*n,1], float)
        for i in range (0,n):
            b[i]= tp[i,0]
            b[i+n]=tp[i,1]
        h = np.linalg.lstsq(m, b, rcond=None)[0]
        self._affineMatrix[0,0]=h[0]
        self._affineMatrix[0,1]=h[1]
        self._affineMatrix[0,2]=h[2]
        self._affineMatrix[1,0]=h[3]
        self._affineMatrix[1,1]=h[4]
        self._affineMatrix[1,2]=h[5]
        self._affineMatrix[2,2]=1
        return True

    def affineTransformation(self):
        channel1 = self._dataFrame[self._dataFrame['channel']==1]
        channel2 = self._dataFrame[self._dataFrame['channel']==2]
        locs = channel2[['x_mean', 'y_mean']].values
        p=np.zeros([3,1])
        p[2]=1
        for i in range (0,channel2.shape[0]):
            p[0]=locs[i,0]
            p[1]=locs[i,1]
            o=np.dot(self._affineMatrix,p)
            locs[i,0]=o[0]
            locs[i,1]=o[1]
        channel2 = channel2.assign(x_mean = locs[:,0])
        channel2 = channel2.assign(y_mean = locs[:,1])
        registeredDataFrame = pd.concat([channel1, channel2])
        registeredDataFrame.plot.scatter(x = 'x_mean',
                                     y= 'y_mean',
                                     c = 'channel',
                                     colormap='viridis')
    
    def saveAffineMatrix(self, prefix='channel2'):
        outname = str('%s/%s_%s_%s' % (self._folderName, self._baseName, prefix,'matrix.csv'))
        header = str('locAligner affine transformation matrix')
        np.savetxt(outname, self._affineMatrix, fmt='%.5f', delimiter=',',header=header,comments='# ')
        print('saved affine matrix to: %s' %(outname))
        