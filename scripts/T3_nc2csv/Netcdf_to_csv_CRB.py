#==============================================================
# conda activate WF24
# WYW,2022
# This code is to transfer NetCDF files to CSV for 
# Task 3 data deliverables.
#===============================================================
import numpy as np
import os, fnmatch
import xarray as xr
import pandas as pd

# assign input and output directory
in_path = "/scratch/04380/wenying/CMIP6/nc2csv/input/"
out_path = "/scratch/04380/wenying/CMIP6/nc2csv/output/"

### read in CRB grids information
df_id = pd.read_csv('./CRB_ID_latlon.txt')

for file in sorted(os.listdir(in_path)):

    if fnmatch.fnmatch(file, '*.nc'):
       file_items=file.split('_')

       var_name  = file_items[0]
       freq_name = file_items[1]
       model_name = file_items[2]
       scenario_name = file_items[3]
       print("processing " +file)

       #read input
       data  =  xr.open_dataset(in_path+"/"+file)
       var_unit = data[var_name].attrs["units"]

       #create dictionary for output structure
       if "day" in freq_name:
           outlist= {'Year': data["time.year"],'Month': data["time.month"],\
                     'Day' : data["time.day"], 'Dayofyear': data["time.dayofyear"]}
       if "mon" in freq_name:
           outlist= {'Year': data["time.year"],'Month': data["time.month"]}
           freq_name = "mon"

       #substract the data to output dataframe for 27 Quad
       unit_convert = 1.
       out_format = "%.2f"

       if "kg m-2 s-1" in var_unit:
         out_format = "%.4f"
         if "day" in freq_name:
            print("mm/s to inch/day")
            unit_convert=  0.0393700787*86400.
         if "mon" in freq_name:
           print("mm/s to inch/mon")
           days = data["time.daysinmonth"]
           unit_convert= 0.0393700787*86400.*days

       print("unit convert = " + str(unit_convert))

       for i in range(df_id.TX_Quad_ID.size):
          outlist[df_id.TX_Quad_ID[i]] = unit_convert*data[var_name].sel(lon=df_id.lon[i], lat=df_id.lat[i], method="nearest")

       #convert to dataframe for writing csv
       subdata=pd.DataFrame(outlist)
       #write output to csv
       outfile="T3_Quad_"+var_name+"_"+freq_name+"_"+model_name+"_"+scenario_name+".csv"
       subdata.to_csv(out_path+outfile, index=False, float_format = out_format)
