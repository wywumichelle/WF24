#!/bin/bash
#SBATCH -J cdo_NAM           # job name
#SBATCH -o cdo_NAM.o%j        # output and error file name (%j expands to jobID)
#SBATCH -N 1               # number of nodes requested
#SBATCH -n 8              # total number of mpi tasks requested
#SBATCH -p normal      # queue (partition) -- normal, development, etc.
#SBATCH -t 00:45:00         # run time (hh:mm:ss) - 1.5 hours
#SBATCH -A A-go3

#===================
# This is the script to regrid the resolution to common 1 degree, and select 1850-2014.
# Run it after
#   combine.sh, for combine multilple time slices to one
#   genwgt.sh , for generate the interpolations weights, which saves time compared to using remapbil
# Run time is about 2 hours for 250 simulations (1980 timesteps)
# WYW, 2021 
#==================

exp="ssp126"
Table="day"
#for vars in pr tas tasmin tasmax ; do
for vars in tasmax ; do

  indir="$SCRATCH/CMIP6/${Table}/${exp}_${vars}/seldate-remap/"
  outdir="$SCRATCH/CMIP6/${Table}/${exp}_${vars}/NAM/"
  mkdir -p $outdir

  while IFS= read -r model; do

    infiles="${vars}_${Table}_${model}_${exp}_*.nc"
    members=$( ls ${indir}${infiles} | cut -d '_' -f 6 )

    for mem in $members; do


      infile=$( ls -1  ${indir}${vars}_${Table}_${model}_${exp}_${mem}_*_*.nc)
      outfile="${outdir}${vars}_${Table}_${model}_${exp}_${mem}_NAM-1_201501-210012.nc"
      echo "$infile -> $outfile"

      cdo -O -L -sellonlatbox,-172.5,-21.5,11.5,76.5 $infile $outfile

 
    done


  done < CMIP6_modellist.txt

done
