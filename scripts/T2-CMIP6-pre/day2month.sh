#!/bin/bash    
##=========================
## Few simulations do not have monthly outputs, but have daily outpus.
## This scripts average the daily values to monthly values.
## instllation of cdo required
## In Cdo, "mean" is equivelant to "nanmean"; "avg" for "mean" (return mssing if any mssing).
##===========================
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 01:00:00
#SBATCH -A A-go3
#SBATCH -p development

cdo monmean  /scratch/04380/wenying/CMIP6/day/ssp126_tasmin/combine/tasmin_day_KACE-1-0-G_ssp126_r1i1p1f1_gr_20150101-21001230.nc\
             /scratch/04380/wenying/CMIP6/mon/ssp126_tasmin/combine/tasmin_Amon_KACE-1-0-G_ssp126_r1i1p1f1_gr_201501-210012.nc


cdo monmean  /scratch/04380/wenying/CMIP6/day/ssp126_tasmax/combine/tasmax_day_KACE-1-0-G_ssp126_r1i1p1f1_gr_20150101-21001230.nc\
             /scratch/04380/wenying/CMIP6/mon/ssp126_tasmax/combine/tasmax_Amon_KACE-1-0-G_ssp126_r1i1p1f1_gr_201501-210012.nc
