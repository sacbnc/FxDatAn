##########################################################
# H E A D E R 
##########################################################
# Name   : Ranges
# Purpose: Produce dataframe of ranges over periods, i.e.
#          average range of all available months for all
#          available years 
# Author : Steve Armstrong
         
##########################################################
# I M P O R T S
##########################################################

import sys
import calendar as cal
import datetime as dt
import numpy as np
import pandas as pd
from itertools import product
import decimal

##########################################################
# M A I N 
########################################################## 

def ranges(df):  
    # Calculate number of decimal places
    times_by = len(str(df['<OPEN>'][0]).split('.')[-1])
    # JPY symbols sometimes have only 1, make it 2 in-line with rest
    if times_by == 1: times_by += 1
    # Get 10 to the power of number of decimals to get proportiante 
    # number to times by to get real number (i.e. integer)
    times_by = 10**times_by
    
    # Get number of available years
    first_year = df.head(1).index.year[0]
    last_year  = df.tail(1).index.year[0]
    
    # Make 2d array of 0's to populate dataframe
    # Use last year+1 as range does not use the upper end
    z = np.zeros(shape=[len(range(first_year, last_year+1)), 12])
    # Use range 1,13 for months as range does not use upper end, same for years
    out_df = pd.DataFrame(z, columns=range(1, 13), index=range(first_year, last_year+1))
    
    # For each year in dataframe
    for year in out_df.index.values:
    
        # For each month in dataframe
        for month in out_df.columns.values:
            total_range = 0
            count = 0
           
            # Get max day of given month for given year
            max_day = cal.monthrange(year, month)[1]
            # Make a temporary dataframe of current month for iteration
            tmp_df = df.ix[dt.date(year, month, 1):dt.date(year, month, max_day)]
            if len(tmp_df) == 0: break
            
            # Calculate range for each given day
            for i in range(0, len(tmp_df)):
                total_range += tmp_df['<HIGH>'][i] - tmp_df['<LOW>'][i]
                count += 1
            
            # Work out average based on total / num of days     
            out_df[month][year] = round((total_range / count) * times_by, 0)
            
    return out_df
        
