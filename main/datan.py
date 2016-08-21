##########################################################
# H E A D E R 
##########################################################
# Name   : Datan
# Purpose: Data analysis tool for financnial instrument data
# Author : Steve Armstrong
         
##########################################################
# I M P O R T S
##########################################################

import os 
import sys
import ntpath
import inspect
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import calendar as cal
import datetime as dt
from itertools import product
import math

DATAN_MASTER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
DATAN_MAIN_DIR   = DATAN_MASTER_DIR + "main/"
DATAN_ALGO_DIR   = DATAN_MASTER_DIR + "algo/"
DATAN_FUNC_DIR   = DATAN_MASTER_DIR + "func/"
DATAN_DATA_DIR   = DATAN_MASTER_DIR + "data/"

# Further imports via path
sys.path.append(DATAN_MAIN_DIR)
sys.path.append(DATAN_ALGO_DIR)
sys.path.append(DATAN_FUNC_DIR)

from confol import confol
from ranges import ranges

##########################################################
# V A R I A B L E S
##########################################################

# DATA FILENAMES
THIS = os.path.abspath(__file__)

# OUTPUT VARS
OUTPUT_TYPES = ["INFO", "WARN", "FAIL"]
OUTPUT_INFO, OUTPUT_WARN, OUTPUT_FAIL = 0,1,2

# DATAFRAME VARS
data_files = []
df_default_cols=['<DATE>', '<TIME>', '<OPEN>', '<LOW>', '<HIGH>', '<CLOSE>']
df_default_index=df_default_cols[0]


##########################################################
# F U N C T I O N S
##########################################################

#---------------------------------------------------------
# FUNCTION output
# Print something to screen, identify if you want an error
# or not

def output(type, location, message):
    if os.path.isfile(location):
        location = location.split('/')[-1]
    print OUTPUT_TYPES[type] + " => " + location + ": " + message

#---------------------------------------------------------
# FUNCTION get_data_dirs
# Construct data frame of all symbols corresponding to periods
# from data available in data directory

def pop_data_dirs():
    data_periods = []
    data_symbols = []
    
    # Check if datan_data_dir is a real dir
    if os.path.isdir(DATAN_DATA_DIR) == False:
        output(OUTPUT_FAIL, inspect.stack()[0][3], "Data dir is not a dir")
        sys.exit(MIN_FOLLOWS1)

    # Get all periods to use for cols
    # Loop through data dir, check the dirs, check they have files
    for item in os.listdir(DATAN_DATA_DIR):
        if os.path.isdir(DATAN_DATA_DIR + item):
            # Check there are files in the directory
            if len(os.listdir(DATAN_DATA_DIR + item)) > 0:
                data_periods.append(item)
                                
    # Get all symbols from all dirs
    for period in data_periods:
        for symbol in os.listdir(DATAN_DATA_DIR + period):
            data_symbols.append(symbol.split('.')[0])
    
    # Remove all dusplicates
    data_symbols = pd.DataFrame(data_symbols)
    data_symbols = data_symbols.drop_duplicates(data_symbols)
    # Make data symbols back into a list
    data_symbols = data_symbols[0].tolist()
    
    # Create 2d array of zeroes to use for initial population of
    # dataframe
    z = np.zeros(shape=[len(data_symbols), len(data_periods)])
    global data_files
    data_files = pd.DataFrame(z, columns=data_periods, index=data_symbols)
    
    for period in data_periods:
        for symbol in data_symbols:
            path = "%s%s/%s.csv" %(DATAN_DATA_DIR, period, symbol)
            if os.path.isfile(path):
                data_files[period][symbol] = 1
                
    output(OUTPUT_INFO, THIS, "available data is:")
    print data_files
                
#---------------------------------------------------------
# FUNCTION get_data_period(period)
# Return a dataframe of all dataframes for specified period

def get_data_period(period):
    data_frames = pd.DataFrame(columns=[period], index=data_files.index.values)
    
    # For each each available symbol
    for symbol in data_files.index.values:
        # If cell for specified period and symbol is 1
        if data_files[period][symbol] == 1:
            # Specify path from the data dir, period (folder) and symbol (filename)
            # and append .csv on the end
            path = "%s%s/%s.csv" %(DATAN_DATA_DIR, period, symbol)
            data_frames[period][symbol] = get_dataframe(path, df_default_cols, df_default_index)
    
    return data_frames
    
##---------------------------------------------------------
# FUNCTION get_data_symbol(symbol)
# Return a dataframe of dataframes for specified symbol

def get_data_symbol(symbol):
    data_frames = pd.DataFrame(columns=data_files.columns.values, index=[symbol])
    
    # For each available timeframe
    for period in data_files.columns.values:
        # If cell for specified period and symbol is 1
        if data_files[period][symbol] == 1:
            path = "%s%s/%s.csv" %(DATAN_DATA_DIR, period, symbol)
            data_frames[period][symbol] = get_dataframe(path, df_default_cols, df_default_index)
    return data_frames

##---------------------------------------------------------
# FUNCTION get_data_symbol_period(symbol, period)
# Return a dataframe for specified symbol and period

def get_data_period_symbol(period, symbol):
    if data_files[period][symbol] == 1:
        path = "%s%s/%s.csv" %(DATAN_DATA_DIR, period, symbol)
        return get_dataframe(path, df_default_cols, df_default_index)

#---------------------------------------------------------
# FUNCTION get_dataframe
# Return a dataframe from filename

def get_dataframe(file, cols, index):
    # Check file is a file
    if not os.path.isfile(file):
        output(OUTPUT_WARN, 
               inspect.stack()[0][3], 
               file + " does not exist")
        
    # Check cols is not empty
    if not cols:
        output(OUTPUT_WARN, 
               inspect.stack()[0][3], 
               "cols is empty")
        
    output(OUTPUT_INFO, 
           THIS, 
           "getting dataframe for " + ntpath.basename(file))
    
    return pd.read_csv(file,
                       index_col=index,
                       parse_dates=True,
                       usecols=cols,
                       na_values=['nan'])

##########################################################
# M A I N 
########################################################## 

output(OUTPUT_INFO, THIS, "initialising")

pop_data_dirs()






