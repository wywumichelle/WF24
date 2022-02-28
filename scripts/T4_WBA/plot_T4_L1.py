#==============================================================
# conda activate WF24
# WYW,2022
# This code is to plot streamflow from models and obs.
# timeseries, pdf, cdf, 
#===============================================================
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy  as np



## read in Watersheds information
df_nf = pd.read_csv('./data/input/Naturalized_Flows.csv')
## read in hydrograph
y = np.array(df_nf["D1"].str.replace(",","").astype(float))
y_cycle = np.average(y.reshape(int(y.size/12),12),0)

##
y_num_zero= len(np.where(y==0.0)[0])



## proccess the hydrograph to histogram (PDF without fitting)
# prepare the bins
range_min = 1.0
range_max = 100000.0
#range_max = np.percentile(y, 95)
#range_max = y.max()
bins_list = np.logspace(np.log10(range_min),np.log10(range_max),num=30)
print(bins_list)
#the fist bins is [0,x), including 1 but excluding x; 


# histogram pdf(density); bin_edges= bins_list
pdf, bin_edges = np.histogram(y,bins=bins_list, density=True)
print(pdf)
## pdf to cdf
cdf = np.cumsum(pdf)


## plot sections
## create 2*2 subplots
fig = plt.figure(figsize=(10,6))
gs = gridspec.GridSpec(2,3, wspace=.5, hspace=.5)

# first plot: monthly time series
ax1= plt.subplot(gs[0,0:2])
bins_list[1] = 1
bins_list[1] = 1
ax1.plot(y)
ax1.set_title("Timeseries")
# second plot: annual cycle
ax2= plt.subplot(gs[0,2])
ax2.plot(y_cycle)
ax2.set_title("Annual Cycle")
## third plot: count of zero streamflow
ax3= plt.subplot(gs[1,0])
ax3.bar(0,y_num_zero)
ax3.set_title("Count of zero flow")

## 4th plot: log space PDF
ax4= plt.subplot(gs[1,1])
ax4.plot(bin_edges[1:],pdf)
ax4.set_xscale('log')
ax4.set_title("PDF")

## 5th plot: log space CDF
ax5 = plt.subplot(gs[1,2])
ax5.plot(bin_edges[1:],cdf)
ax5.set_xscale('log')
ax5.set_title("CDF")

fig.suptitle("D1 Colorado River at Winchell", fontweight ="bold")

plt.savefig('test.pdf')



