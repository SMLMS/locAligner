#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 17:44:22 2019

@author: malkusch
"""

from ipywidgets import widgets
from ..jupyter import laWidgets

class LaRegisterWidgets(laWidgets.LaWidgets):
    def __init__(self):
        laWidgets.LaWidgets.__init__(self)
# =============================================================================
#         self.pathText = self.createPathText()
#         self.pathButton = self.createPathButton()
#         self.nText = self.createTextInt(val=0, minVal=0, maxVal=100, stepSize=1, desc="n")
#         self.p0Text = self.createTextInt(val=1, minVal=0, maxVal=100, stepSize=1, desc="p0")
#         self.mText = self.createTextInt(val=1, minVal=0, maxVal=100, stepSize=1, desc="m")
#         self.pText = self.createTextFloat(val=0.3, minVal=0.0, maxVal=1.0, stepSize=0.001, desc="p")
#         self.initDText = self.createTextFloat(val=0.3, minVal=0.0, maxVal=1.0, stepSize=0.001, desc="initD")
#         self.initDSlider = self.createSliderFloat(val=0.3, minVal=0.0, maxVal=1.0, stepSize=0.001, desc="initD")
#         self.initDLink = self.createLink(self.initDText, self.initDSlider)
#         self.analysisButton = self.createButton(desc = 'run Analysis')
# =============================================================================
        self.loadButton = self.createButton(desc = 'load')
        self.dbscanButton = self.createButton(desc = 'DBSCAN')
        self.minSampleText = self.createTextInt(val=5, minVal=0, maxVal=500, stepSize=1, desc="min_Samples")
        self.epsText = self.createTextFloat(val=10.0, minVal=0.0, maxVal=1000.0, stepSize=0.1, desc="eps")
        self.channelSelector = self.createSelector(opt=['1', '2'],val='1', desc='channel')
        self.clusterSelector = self.createDropDown(desc='cluster')
        self.visClusterButton = self.createButton(desc = 'plot cluster')
        self.min_x_filter_text = self.createTextInt(val=0, minVal=0, maxVal=45000, stepSize=1, desc="min x [nm]")
        self.max_x_filter_text = self.createTextInt(val=45000, minVal=0, maxVal=45000, stepSize=1, desc="max x [nm]")
        self.x_filter = widgets.HBox((self.min_x_filter_text, self.max_x_filter_text))
        self.min_stdX_filter_text = self.createTextFloat(val=0.0, minVal=0.0, maxVal=1000.0, stepSize=0.1, desc="min std_x [nm]")
        self.max_stdX_filter_text = self.createTextFloat(val=30.0, minVal=0.0, maxVal=1000.0, stepSize=0.1, desc="max std_x [nm]")
        self.stdX_filter = widgets.HBox((self.min_stdX_filter_text, self.max_stdX_filter_text))
        self.min_y_filter_text = self.createTextInt(val=0, minVal=0, maxVal=81000, stepSize=1, desc="min y [nm]")
        self.min_y_filter_text = self.createTextInt(val=0, minVal=0, maxVal=81000, stepSize=1, desc="min y [nm]")
        self.max_y_filter_text = self.createTextInt(val=81000, minVal=0, maxVal=81000, stepSize=1, desc="max y [nm]")
        self.y_filter = widgets.HBox((self.min_y_filter_text, self.max_y_filter_text))
        self.min_stdY_filter_text = self.createTextFloat(val=0.0, minVal=0.0, maxVal=1000.0, stepSize=0.1, desc="min std_y [nm]")
        self.max_stdY_filter_text = self.createTextFloat(val=30.0, minVal=0.0, maxVal=1000.0, stepSize=0.1, desc="max std_y [nm]")
        self.stdY_filter = widgets.HBox((self.min_stdY_filter_text, self.max_stdY_filter_text))
        self.min_int_filter_text = self.createTextInt(val=0, minVal=0, maxVal=10000, stepSize=1, desc="min int")
        self.max_int_filter_text = self.createTextInt(val=10000, minVal=0, maxVal=10000, stepSize=1, desc="max int")
        self.int_filter = widgets.HBox((self.min_int_filter_text, self.max_int_filter_text))
        self.min_area_filter_text = self.createTextInt(val=0, minVal=0, maxVal=1000, stepSize=1, desc="min area [nm\u00B2]")
        self.max_area_filter_text = self.createTextInt(val=1000, minVal=0, maxVal=1000, stepSize=1, desc="max area [nm\u00B2]")
        self.area_filter = widgets.HBox((self.min_area_filter_text, self.max_area_filter_text))
        self.filterButton = self.createButton(desc='Filter Fiducials')
        self.visFiducialButton = self.createButton(desc='plot fiducials')
        self.x_shift_float = self.createSliderFloat(val=0.0, minVal=-2000.0, maxVal=2000.0, stepSize=1.0, ori='horizontal', desc="dx")
        self.y_shift_float = self.createSliderFloat(val=0.0, minVal=-2000.0, maxVal=2000.0, stepSize=1.0, ori='vertical', desc="dy")
        self.shift = widgets.HBox((self.y_shift_float, self.x_shift_float))
        self.thr_dist = self.createTextInt(val=250, minVal=0, maxVal=1000, stepSize=1, desc="distance threshold [nm]")
        self.matrixButton = self.createButton(desc = 'create matrix')
        self.outFilePrefix = self.createTextStr(value='channel2', desc='file prefix', placeHolder = 'channel2')
        self.saveButton = self.createButton(desc = 'save matrix')
    
    def createPathText(self):
        text = self.createTextStr(value='', desc='path to file')
        text.observe(self.updateFileName)
        return text
    
    def createPathButton(self):
        button = self.createButton(desc = 'browse')
        button.on_click(self.browseFile)
        return button            