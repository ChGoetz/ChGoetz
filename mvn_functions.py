#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 14:57:19 2021

@author: charlotte gotz

Define a couple functions that are useful to analyse MAVEN data


"""

import datetime as dt
import pandas as pd
import numpy as np
from os import path

# =============================================================================
# LOAD DATA
# =============================================================================
def load_mag(year,month,day):
    
    day_to_load = dt.datetime(year,month,day)
    
    filepath = '/Users/charlotte gotz/andere_missionen/maven/' + day_to_load.strftime('%Y/%m') + '/'    
    filename = 'mvn_mag_l2_' + day_to_load.strftime('%Y%j') + 'ss1s_' + day_to_load.strftime('%Y%m%d') + '_v01_r01.sts'
    
    # =============================================================================
    # first, find length of header 
    # =============================================================================
    string1 = 'OUTBOARD_BD_PAYLOAD'
    file1 = open(filepath + filename, 'r')
    index = 0
    # Loop through the file line by line
    for line in file1:  
        index = index + 1 
        # checking string is present in line or not
        if string1 in line:
          break     
    file1.close() 
    
    
    # =============================================================================
    # now load data and convert to a useful dateformat, drop unused variables
    # =============================================================================
    VariableNames = ["year", "doy", "hr", "min", "sec", "msec", "dday", "Bx", "By", "Bz", "range", "x", "y", "z", "Bx_pl", "By_pl", "Bz_pl", "range_pl"]
    mag = pd.read_table(filepath + filename,header=index+24,sep='\s+',names = VariableNames)
    
    mag['year'] = pd.to_datetime(mag['dday']-1, unit='D', origin=str(mag['year'][0]))
    mag['doy'] = np.sqrt(mag.Bx**2 + mag.By**2 + mag.Bz**2) # add the magnetic field magnitude
    
    mag.rename(columns={'year':'t','doy':'Bm'}, inplace = True)
    #del mag[['hr', "min", "sec", "msec", "dday"]] #this should do the same as drop
    mag = mag.drop(["hr", "min", "sec", "msec", "dday"], axis=1)
    
    
    return mag
