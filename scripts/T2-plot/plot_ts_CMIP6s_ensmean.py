#==============================================================
# conda activate WF24
# WYW,2021
#===============================================================
import numpy as np
import cftime
import matplotlib.pyplot as plt
#from netCDF4 import Dataset
import os, fnmatch
import xarray as xr
import nc_time_axis


model_name = list()
with open("../tools/CMIP6_modellist.txt", "r") as f:
  for line in f:
    model_name.append(line[:-1])

data_dir = "/scratch/04380/wenying/CMIP6/mon/historical_tas/ensmean"

for i  in  range(len( model_name)):
  
  filename = fnmatch.filter(os.listdir(data_dir),"*"+model_name[i]+"*.nc")
  data = xr.open_dataset(data_dir+"/"+str(filename[0]))
#print(data.variables.keys())
  #subset=data.sel(lat=30.3208,lon=-97.7604,method='nearest')
  # Slice the data spatially using a single lat/lon point
  #y = subset.variables['tas'][:]
  #x = subset.variables['time'][:]
  one_point = data['tas'].sel(lat=30.3208,lon=-97.7604,method='nearest')
  y = one_point.resample(time="1YS").mean()

  plt.figure(figsize=(8,6))
  one_point.plot.line(label="monthly")
  y.plot.line(label="yearly")
  
  plt.ylim(270,310)
  plt.xlabel(str(filename[0])) 
  plt.ylabel("Temperature (K)") 
  plt.title(model_name[i]+"@ Austin Camp Mabry")
  plt.legend()
#plt.show() 
  plt.savefig(model_name[i]+"_ensmean_ts.png")
  data.close()
  plt.close()
