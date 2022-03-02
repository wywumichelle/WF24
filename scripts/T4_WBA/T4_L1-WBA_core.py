#==============================================================
# conda activate WF24
# WYW,2022
# This code is to caculate streamflow from CMIP6 *runoff
# A simple water balance approach.
#===============================================================
import numpy as np
import os, fnmatch
import xarray as xr
import pandas as pd

## assign input and output directory
csv_in_path = "./data/input/"
nc_in_path = "/scratch/04380/wenying/CMIP6/T4_WBA/input/"
out_path = "./data/output/"

## read in Watersheds-grids information
df_id = pd.read_csv(csv_in_path +'Dissolved_Watersheds_on_Grids.csv')

#all_Quad_ID  = df_id.TX_QUAD_ID
all_Quad_lat = np.array(df_id.lat)
all_Quad_lon = np.array(df_id.lon)
all_CP_ID    = df_id.CP_ID
all_poly_area= np.array(df_id.Area_sqkm)
#CP_ID: A1..K2 (K1=outlet)

## read in Watersheds information; use the order of gagues in this file
df_ws = pd.read_csv(csv_in_path + 'WAM_control_point_name.csv')
df_ws = df_ws.sort_values(by=["CP_ID"], ascending=True)
df_ws = df_ws.reset_index(drop=True)
CP_ID    = df_ws.CP_ID



for file in sorted(os.listdir(nc_in_path)):

    if fnmatch.fnmatch(file, '*global-1-n*.nc'):

        file_items=file.split('_')

        file_items=file.split('_')
        model_name = file_items[2]
        scenario_name = file_items[3]
        
        ## read nc input
        data  =  xr.open_dataset(nc_in_path+"/"+file)
        out_path="./"
        ## prepare output CSV files
        outfile="T4_NCP_Flows_L1_mon_"+model_name+"_"+scenario_name+".csv"
        outlist= {'Year': data["time.year"],'Month': data["time.month"]}
        
        ## Q = R*A
        ## loops for each control points(43)
        for i in range(CP_ID.size):
          ID = CP_ID[i]
          locs = [loc for loc, x in enumerate(all_CP_ID) if x == ID] 
          Quad_lat  = xr.DataArray(all_Quad_lat[locs],dims="points")
          Quad_lon  = xr.DataArray(all_Quad_lon[locs],dims="points")
          Poly_area = all_poly_area[locs]
        
          runoff =  data.mrro.sel(lon=Quad_lon, lat=Quad_lat, method="nearest")
          # replace negative runoff with zero
          # https://xarray.pydata.org/en/stable/generated/xarray.DataArray.where.html#
          runoff = runoff.where(runoff>0,0)
        
        
          #=========unit coversion
          # "[kg m-2 s-1]*sq.km" to "acre-feet/month"
          # acre-foot = 1,233.48183754752 m3
          # 1 month   = 86400s*days
          # (86400*days*10^-3*10^3*10^3)/1,233.48183754752 = 70045.6199434*days
          days        =  data["time.days_in_month"]
          unit_cvt =  70045.6199434*days
          #=======(time)*(time,pts)==
          runoff_cvt =  unit_cvt*runoff
          #=======(pts)*(time,pts)===
          Q = Poly_area*runoff_cvt
          #=====summation of grids(pts)===
          Q_sum = Q.sum(dim="points")
          Q_sum_avg= Q_sum.mean(dim="time")
        #  print(ID+":"+str(Q_sum_avg.values))
          outlist[ID] = Q_sum
        
        print(model_name+"_"+scenario_name+"_"+ID+" avg:"+str(Q_sum_avg.values))
        
        #convert to dataframe for writing csv
        subdata=pd.DataFrame(outlist)
        subdata=subdata.astype(int)
        #write output to csv
        subdata.to_csv(out_path+outfile, index=False)
