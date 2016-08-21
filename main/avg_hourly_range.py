##########################################################
# H E A D E R 
##########################################################
# Name   : Average Ranged
# Purpose: Calculate average range of each month of each year
#          for all available symbols
#          Plot each symbols results in a heatmap subplot,
#          displaying all graphs in a grid
# Author : Steve Armstrong
         
##########################################################
# I M P O R T S
##########################################################

from datan import *

##########################################################
# M A I N 
########################################################## 

# Set empty axes list
axes = []

fig = plt.figure(figsize=(25,12))
fig.suptitle("Forex Majors: average hourly pip range per month per year", fontsize=20)

# Get all hourly data from main 
data_frames = get_data_period('1h')

num_plots = len(data_frames)

# Have to define as float to force math.ceil to take upper value
# otherwise is computed as int and automatically rounded down
fig_cols = 5.0
fig_rows = math.ceil(num_plots / fig_cols) 

# Loop through data dataframe 
for idx, symbol in enumerate(data_frames.index.values):
    
    output(OUTPUT_INFO, os.path.abspath(__file__), "processing " + symbol)

    df = data_frames['1h'][idx]
    
    ranges_df = ranges(df)
    
    # Define x and y as the length of columns and indices for use in setting
    # x and y ticks
    x, y = len(ranges_df.columns.values), len(ranges_df.index.values)
    
    # Number of rows, number of cols, region ordinal

    axes.append(fig.add_subplot(fig_rows, fig_cols, idx+1))
    
    # Get axes from imshow
    axes[idx].imshow(ranges_df, interpolation='nearest', cmap='Oranges', aspect='auto')

    # Set values for x/y ticks/labels
    axes[idx].set_xticks(np.linspace(0, x-1, x))
    axes[idx].set_xticklabels(ranges_df.columns)
    axes[idx].set_yticks(np.linspace(0, y-1, y))
    axes[idx].set_yticklabels(ranges_df.index)
    
    # Hide grid lines and set title
    axes[idx].grid('off')
    axes[idx].set_title(symbol, y=-0.08)
    # Push x axis to top instead of bottom
    axes[idx].xaxis.tick_top()
    axes[idx].autoscale(False)
    
    # Set text in middle of each heat square to it's corresponding value 
    for i, j in product(range(y), range(x)):
        axes[idx].text(j, i, '{0:.0f}'.format(ranges_df.iloc[i, j]),
            size='small', ha='center', va='center')

plt.show()




