#==============================================================
# conda activate WF24
# WYW,2021
# This code is to produce climate extreme indices (cei) 
# from daily max temp (tasmax) fields.
#===============================================================
#from xhistogram.xarray import histogram
import numpy as np
import os, fnmatch
import xarray as xr

# assign input and output directory
in_path = "/scratch/04380/wenying/CMIP6/tasmax-cei/input"
out_path = "/scratch/04380/wenying/CMIP6/tasmax-cei/output"

for file in os.listdir(in_path):
    if fnmatch.fnmatch(file, '*.nc'):
       #remane output file name [tasmax_day] to [tasmax-cei_yr]
       outfile="tasmax-cei_yr"+file[10:]
       print("processing " +file)

       #read input
       data  =  xr.open_dataset(in_path+"/"+file)
       
       # hot days above 90 F (32.22C; 305.372222K)
       odata = data.tasmax.where(data.tasmax >= 305.372222).resample(time='1Y').count(dim='time')
       odata.name= 'tasmax_g90f'
       odata.attrs['long_name'] = "Yearly hot days with tasmax larger than 90F (~32.22C)"
       
       # dataarray to dataset (xarray)
       ods = odata.to_dataset()

       # hot days above 95F (35.00C;308.15K)
       tasmax_g95f=data.tasmax.where(data.tasmax  >= 308.15).resample(time='1Y').count(dim='time')
       tasmax_g95f.attrs['long_name'] = "Yearly hot days with tasmax larger than 95F (35.00C)"
       ods['tasmax_g95f'] =tasmax_g95f
       
       # hot days above 100F (37.78C;310.927778K) 
       tasmax_g100f=data.tasmax.where(data.tasmax >= 310.927778).resample(time='1Y').count(dim='time')
       tasmax_g100f.attrs['long_name'] = "Yearly hot days with tasmax larger than 100F (~37.78C)"
       ods['tasmax_g100f'] =tasmax_g100f
       
       # hot days above 104F (40C;313.15K)
       tasmax_g104f=data.tasmax.where(data.tasmax >= 313.15).resample(time='1Y').count(dim='time')
       tasmax_g104f.attrs['long_name'] = "Yearly hot days with tasmax larger than 104F (40.00C)"
       ods['tasmax_g104f'] =tasmax_g104f

       # hot days above 105F (40.56C;313.705556K)
       tasmax_g105f=data.tasmax.where(data.tasmax >= 313.705556).resample(time='1Y').count(dim='time')
       tasmax_g105f.attrs['long_name'] = "Yearly hot days with tasmax larger than 105F (~40.56C)"
       ods['tasmax_g105f'] =tasmax_g105f


       #  Number of icing days: days when daily tasmax < 0°C
       tasmax_l32f =data.tasmax.where(data.tasmax < 273.15).resample(time='1Y').count(dim='time')
       tasmax_l32f.attrs['long_name'] = "Yearly icing days(ID) with tasmax smaller than freezing point"
       ods['tasmax_l32f'] =tasmax_l32f

       
       # number of day in each year; days(year)
       # bacuase CMIP6 models use different calendar
       ods['dayinyear'] = data.time.resample(time='1Y').count(dim='time')
       ods.dayinyear.attrs['long_name'] = "Number of days in each year" ;
       
       # write ouput file
       ods.to_netcdf(out_path+"/"+outfile)

