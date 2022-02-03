#==============================================================
# conda activate WF24
# WYW,2021
# This code is to produce climate extreme indices (cei) 
# from daily precipiation (pr) fields.
#===============================================================
#from xhistogram.xarray import histogram
import numpy as np
import cftime
import matplotlib.pyplot as plt
#from netCDF4 import Dataset
import os, fnmatch
import xarray as xr
import nc_time_axis

# assign input and output directory
in_path = "/scratch/04380/wenying/CMIP6/day/historical_pr/NAM"
out_path = "/scratch/04380/wenying/CMIP6/pr-cei"

for file in os.listdir(in_path):
    if fnmatch.fnmatch(file, '*.nc'):
       #remane output file name [pr_day] to [pr-cei_yr]
       outfile="pr-cei_yr"+file[6:]
       print("proccessing " +file)

       #read input
       data  =  xr.open_dataset(in_path+"/"+file)
       
       # convert precipitaiton units mm/s to mm/day
       data['pr']=data['pr']*86400.
       
       # dry day smaller than 1 mm
       odata = data.pr.where(data.pr <= 1.).resample(time='1Y').count(dim='time')
       odata.name= 'dryday_1mm'
       odata.attrs['long_name'] = "Yearly dry days with precipitation less than 1mm (~0.04inch)"
       
       # dataarray to dataset (xarray)
       ods = odata.to_dataset()
       
       # dry day smaller than 0.01 inch (0.254mm)
       dryday=data.pr.where(data.pr <= .254).resample(time='1Y').count(dim='time')
       dryday.attrs['long_name'] = "Yearly dry days with precipitation less than 0.254mm (0.01inch)"
       ods['dryday'] = dryday
       
       
       # wet day larger than 1 inch
       wetday_1inch = data.pr.where(data.pr >= 25.4).resample(time='1Y').count(dim='time')
       wetday_1inch.attrs['long_name'] = "Yearly wet days with precipitation larger than 25.4mm (1inch)"
       ods['wetday_1inch'] = wetday_1inch
       
       # wet day larger than 2 inch
       wetday_2inch = data.pr.where(data.pr >= 50.8).resample(time='1Y').count(dim='time')
       wetday_2inch.attrs['long_name'] = "Yearly wet days with precipitation larger than 50.8mm (2inch)"
       ods['wetday_2inch'] = wetday_2inch
       
       # wet day larger than 3 inch
       wetday_3inch = data.pr.where(data.pr >= 76.2).resample(time='1Y').count(dim='time')
       wetday_3inch.attrs['long_name'] = "Yearly wet days with precipitation larger than 76.2mm (3inch)"
       ods['wetday_3inch'] = wetday_3inch
       
       # number of day in each year; days(year)
       # bacuase CMIP6 models use different calendar
       ods['dayinyear'] = data.time.resample(time='1Y').count(dim='time')
       ods.dayinyear.attrs['long_name'] = "Number of days in each year" ;
       
       # write ouput file
       ods.to_netcdf(out_path+"/"+outfile)

