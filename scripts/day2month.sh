#!/bin/bash    
##=========================
## Few simulations do not have monthly outputs, but have daily outpus.
## This scripts average the daily values to monthly values.
## instllation of cdo required
## In Cdo, "mean" is equivelant to "nanmean"; "avg" for "mean" (return mssing if any mssing).
##===========================
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 00:02:00
#SBATCH -A A-go3
#SBATCH -p development

cdo monmean /scratch/04380/wenying/CMIP6/day/historical_pr/pr_day_KIOST-ESM_historical_r1i1p1f1_gr1_18500101-20141231.nc \
            /scratch/04380/wenying/CMIP6/mon/historical_pr/pr_Amon_KIOST-ESM_historical_r1i1p1f1_gr1_185001-201412.nc 
