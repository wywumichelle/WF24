#==============================================================
# conda activate WF24
# scripts modified from
# https://help.ceda.ac.uk/article/4728-cru-data-python-example
# WYW,2021
#===============================================================
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from  mpl_toolkits.basemap import Basemap
import os, fnmatch
import csv

model_name = list()
with open("../tools/CMIP6_modellist.txt", "r") as f:
  for line in f:
    model_name.append(line[:-1])

data_dir = "/scratch/04380/wenying/CMIP6/mon/historical_tas/ensmean"


for i  in  range(len( model_name)):
  
  filename = fnmatch.filter(os.listdir(data_dir),"*"+model_name[i]+"*.nc")
  data = Dataset(data_dir+"/"+str(filename[0]))
#print(data.variables.keys())

  temp = data.variables['tas'][:]
  temp_av_1850_2014= np.mean(temp[:,:,:],axis = 0)

  plt.figure(figsize=(8,6))
  map = Basemap(projection="cyl", resolution='c', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180) 
  map.drawcoastlines(color="black") 
  lons,lats = np.meshgrid(data.variables['lon'][:], data.variables['lat'][:]) 
  x,y = map(lons, lats)

  temp_plot = map.contourf(x, y, temp_av_1850_2014, cmap='coolwarm') 
  plt.title(model_name[i])
  plt.annotate('ens',(-178,-88), fontsize=6)
  plt.clim([233.15,313.15])
  plt.annotate(str(filename[0]),(-178,-88), fontsize=8)
  cb = map.colorbar(temp_plot, "bottom", size="5%", pad="2%")
  cb.set_label(u"Temperature (K)")
#plt.show() 
  plt.savefig(model_name[i]+"_global.png")
  data.close()
  plt.close()
