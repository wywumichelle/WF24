#==============================================================
# conda activate WF24
# WYW,2021
# This code is to produce climate extreme indices (cei) 
# from daily max temp (tasmin) fields.
#===============================================================
import numpy as np
import os, fnmatch
import xarray as xr

# assign input and output directory
in_path = "/scratch/04380/wenying/CMIP6/tasmin-cei"
out_path = "/scratch/04380/wenying/CMIP6/tasmin-cei/output"

for file in os.listdir(in_path):
    if fnmatch.fnmatch(file, '*.nc'):
       #remane output file name [tasmin_day] to [tasmin-cei_mon]
       outfile="tasmin-cei_mon"+file[10:]
       print("processing " +file)

       #read input
       data  =  xr.open_dataset(in_path+"/"+file)
       
       # Days w/tasmin above 90 F (32.22C; 305.372222K)
       odata = data.tasmin.where(data.tasmin >= 305.372222).resample(time='1M').count(dim='time')
       odata.name= 'tasmin_g90f'
       odata.attrs['long_name'] = "Monthly days with tasmin larger than 90F (~32.22C)"
       
       # dataarray to dataset (xarray)
       ods = odata.to_dataset()

       # Days w/tasmin above 80F (26.67C;299.816667K)
       tasmin_g80f=data.tasmin.where(data.tasmin  >= 299.816667).resample(time='1M').count(dim='time')
       tasmin_g80f.attrs['long_name'] = "Monthly days (warm nights) with tasmin larger than 80F (~26.67C)"
       ods['tasmin_g80f'] =tasmin_g80f
       
       tasmin_l32f =data.tasmin.where(data.tasmin < 273.15).resample(time='1M').count(dim='time')
       tasmin_l32f.attrs['long_name'] = "Monthly frost days (cold nights) with tasmin smaller than freezing point"
       ods['tasmin_l32f'] =tasmin_l32f

       
       # number of day in each month; days(month)
       # bacuase CMIP6 models use different calendar
       ods['dayinmonth'] = data.time.resample(time='1M').count(dim='time')
       ods.dayinmonth.attrs['long_name'] = "Number of days in each month" ;
       
       # write ouput file
       ods.to_netcdf(out_path+"/"+outfile)

