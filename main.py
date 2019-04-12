# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 09:29:10 2019

@author: malkusch
"""
from locAligner.data import localizations
from locAligner.data import fiducials


def main():
    locDataSet = localizations.SMLM_localizations()
    locDataSet.browseFile()
    locDataSet.updateNames()
    locDataSet.importData()
    locDataSet.clusterLocalizations()
    clDataSet = fiducials.SMLM_fiducials()
    clDataSet.createClusterDataSet(locDataSet.dataFrame)
    clDataSet.viewData()
    locDataSet.plotLocalizations()
    locDataSet.plotCluster(30)
    clDataSet.plotFiducials()
    
    
if __name__ == '__main__':
    main()