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

## define select years
start_yr= 1950
end_yr  = 2014
time_ax = pd.date_range('1950-01','2015-01', freq='M')
##

## read in Watersheds information (Name)
df_ws = pd.read_csv('./data/input/WAM_control_point_name.csv')
df_ws = df_ws.sort_values(by=["CP_ID"], ascending=True)
df_ws = df_ws.reset_index(drop=True)
CP_ID    = df_ws.CP_ID
CP_name = df_ws.Description
 

## read in 43 Flows timeseries
df_nf = pd.read_csv('./data/input/Naturalized_Flows.csv')
df_nf = df_nf.loc[(df_nf['Year'] >= start_yr) & (df_nf['Year']<= end_yr)]


# prepare the bins
range_min = 1.0
range_max = 10000000.0
#range_max = np.percentile(y, 95)
#range_max = y.max()
bins_list = np.logspace(np.log10(range_min),np.log10(range_max),num=30)
#the fist bins is [0,x), including 1 but excluding x;


for i in range(CP_ID.size):

  ID = CP_ID[i]
  print(ID)

  ## read in hydr graph
  y = np.array(df_nf[ID].str.replace(",","").astype(float))
  y_cycle = np.average(y.reshape(int(y.size/12),12),0)

  ## count zero flow
  y_num_zero= len(np.where(y==0.0)[0])



  ## proccess the hydrograph to histogram (PDF without fitting)
  bins_list = np.logspace(np.log10(range_min),np.log10(range_max),num=30)
  #the fist bins is [0,x), including 1 but excluding x; 

  # histogram pdf(density); bin_edges= bins_list
  hist, bin_edges = np.histogram(y,bins=bins_list)
  # count to probability
  pdf = hist/y.size
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
  ax1.plot(time_ax,y)
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

  fig.suptitle(ID +": "+ CP_name[i], fontweight ="bold")

  plt.savefig("./fig/T4_L1_NF_"+ID+'.pdf')
  plt.close('all')
