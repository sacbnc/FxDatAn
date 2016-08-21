##########################################################
# H E A D E R 
##########################################################
# Name   : Consecutive Follows 
# Purpose: Essentially a wrapper to run confol() on multiple
#          symbols
# Author : Steve Armstrong
         
##########################################################
# I M P O R T S
##########################################################

from datan import *

DATAN_MAIN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DATAN_MAIN_DIR)

##########################################################
# M A I N 
########################################################## 

period = '1h'
data_frames = get_data_period(period)
confols = []

# Set figure size
fig = plt.figure(figsize=(25,12))
    
for symbol in data_frames.index.values:
    output(OUTPUT_INFO, sys.argv[0], "getting confol for " + symbol)
    confols.append(confol(data_frames[period][symbol], 1, 200))
    plt.plot(confols[len(confols)-1], label=symbol)

# Calculate biggest len of each confol list in confols
max_len = 0
for list in confols:
    if len(list) > max_len:
        max_len = len(list)
  
# Calculate smallest and largest value in all lists
lowest_value = 100
highest_value = 0

for list in confols:
    # Calculate from 1st element to ignore 0 at index 0
    for elem in list[1:]:
        if elem < lowest_value: lowest_value = elem
        if elem > highest_value: highest_value = elem 
    
# Present
plt.ylim(lowest_value, highest_value)
plt.xlim(1,max_len)
plt.xticks(range(1, max_len))
plt.legend(loc='lower right')
plt.xlabel('Number of consecutive bull candles', fontsize=15)
plt.ylabel('% chance of another bull candle following', fontsize=15)
plt.title('CONFOL of Forex majors')

plt.show()


    


    