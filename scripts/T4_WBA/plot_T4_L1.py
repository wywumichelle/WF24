#==============================================================
# conda activate WF24
# WYW,2022
# This code is to plot streamflow from models and obs.
# (a) timeseries (b) py (c) CDF
#===============================================================
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy  as np



## read in Watersheds information
df_nf = pd.read_csv('./data/input/Naturalized_Flows.csv')
## read in hydrograph
y = np.array(df_nf["K1"].str.replace(",","").astype(float))
y_cycle=

## proccess the hydrograph to histogram (PDF without fitting)
# prepare the bins
range_min = 0.1
range_max = y.max()
bins_list = np.logpace(log10(range_min),log10(range_max),num=30)
print(bins_list)
#the fist bins is [0,x), including 1 but excluding x; last bins

# histogram pdf(density); bin_edges= bins_list
pdf, bin_edges = np.histogram(y,bins=bins_list, density=True)

## pdf to cdf
cdf = np.cumsum(pdf)


## plot sections
## create 2*2 subplots
gs = gridspec.GridSpec(3,3)

# first plot: monthly time series
ax1= plt.subplot(gs[0,0:1])
ax1.plot(y)

# second plot: annual cycle
ax2= plt.subplot(gs[0,2])
ax2.plot(y_cycle)

## third plot: count of zero streamflow
ax3= plt.subplot(gs[1,0])
ax3.plot(y_zero,kind='bar')

## 4th plot: log space PDF
ax4= plt.subplot(gs[1,1])
ax4.plot(bin_edges[1:],pdf)
# set_xscale log

## 5th plot: log space CDF
ax5 = plt.subplot(gs[1,1])
ax5.plot(bin_edges[1:],cdf)




plt.savefig('test.pdf')



