##########################################################
# H E A D E R 
##########################################################
# Name   : Consequctive Candle Occurance Follow-up
# Purpose: Identify % chance of a candle of particular
#          direction occuring after a chain of n candles 
#          occured in that same direction
# Author : Steve Armstrong
         
##########################################################
# V E R S I O N 
##########################################################
# VERS AUTH  DATE              CHANGES
# --------------------------------------------------------
# 0.1  SRA  080816   Pulled from datan.py and imported
#                    all of datan.py
# 0.2  SRA  110816   Solidified algorithm with dynamic array
#                    allocation to allow for any amount of 
#                    candle sequences, despire the general rule
#                    that the more the smaller the sample size 
#                    thus the credibility. 
#                    Changed into a function format 

##########################################################
# I M P O R T S
##########################################################

import sys
from matplotlib import pyplot as plt

##########################################################
# M A I N 
########################################################## 

#datan.output(OUTPUT_INFO, "confol", "init confol")
           
def confol(df, min_candles, min_sample_size):
    # Mimimum candles want to count, i.e. if == to 1 then we 
    # want to know when a single candle occurs
        
    # Minimum candles we want to see occur in a chain before we
    # observe them. This must always be equal to min_candles + 1
    # as you always want to know what the chances of another candle
    # in same direction appearing is for each possible sequence of
    # same-direction candles
    min_follows = min_candles + 1

    higher_count      = 0
    higher_occurances = [0]
    higher_follows    = [0]
    
    for i in range(1, len(df)):
        if df['<CLOSE>'][i] > df['<OPEN>'][i]:
            
            higher_count += 1
            
            # If the length of list is smaller than the below values
            # then you want to increase list size by 1
            if len(higher_occurances) <= higher_count - min_candles:
                higher_occurances.append(0)
            if len(higher_follows)    <= higher_count - min_follows:
                higher_follows.append(0)
            
            # If the number of candles (higher_count) is <= min_candles
            # then increment the according array element
            # for example, if 3 is our min number of candles, we will start
            # at index 0 which will represent 3 candles, then upwards
            if higher_count >= min_candles:
                higher_occurances[higher_count-min_candles] += 1
            
            # The same applies for below, but as min_follows is always 
            # equal to min_candles +1, an array index of one below is always
            # incremeneted
            # for example, if min_candles is 1 then and higher_count is 1, 
            # then higher_occurances[0] is incremeneted, but higher_follows[0]
            # is not incremented until higher_count is == 2, indicating another
            # occurance of a higher candle appearing after 1 higher candle
            if higher_count >= min_follows: 
                higher_follows[higher_count-min_follows] += 1
        else:
            higher_count = 0
    
    
    # Append higher_follows with 0, as the max sequence of candles
    # would not have a follow on candle and thus thus the list
    # are not of equal size
    higher_follows.append(0)
    
    # Now remove any elements that do not meet the minimum sample size
    # Only look at higher_occurances for this, as we would still want to 
    # know if a sequence occured 1000 times but only had 5 following candles
    i=0
    while i < len(higher_occurances): 
        # Make scanned_all equal to True, if a hit is found in the below
        # loop then it's set to false, indicating there is potentially another
        # to find
        for j in range(0, len(higher_occurances)):
            if higher_occurances[j] < min_sample_size:
                higher_occurances.pop(j)
                higher_follows.pop(j)
                i=j
                break
    
    # Create a list of same size as higher_occurances
    higher_chances = []
    follow_count = 0.0
    revert_count = 0.0
    
    # Loop through each occurance and calculate the chance of a follow on
    # by (# of follows from sequence of n candles) / (# number of occurances of 
    #     sequence of n candles)
    for i in range(0, len(higher_occurances)-1):
        higher_chances.append(0)
        
        follow_count = higher_follows[i]
        occurance_count = higher_occurances[i]
        
        higher_chances[i] = float(follow_count) / float(occurance_count) 
    
    # Round higher chances to 2 decimal places
    
    # Inset 0 at first index so index 1 reflect sequence of 1 candle
    higher_chances.insert(0, 0)
    
    # Convert to actual percentages for presentation
    higher_chances = [ elem*100 for elem in higher_chances]
    # Round all floats to 2 decimal places
    higher_chances = [ round(elem, 2) for elem in higher_chances ]
    return higher_chances


