#!/bin/bash
#SBATCH -J cdo_selmap           # job name
#SBATCH -o cdo_selmap2.sh        # cdo_selmap.o%j output and error file name (%j expands to jobID)
#SBATCH -N 2               # number of nodes requested
#SBATCH -n 48              # total number of mpi tasks requested
#SBATCH -p normal      # queue (partition) -- normal, development, etc.
#SBATCH -t 00:05:00         # run time (hh:mm:ss) - 1.5 hours
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
Table="Lmon"
for vars in mrro ; do
#for vars in pr tas tasmin tasmax ; do

  indir="$SCRATCH/CMIP6/mon/${exp}_${vars}/combine/"
  outdir="$SCRATCH/CMIP6/mon/${exp}_${vars}/seldate-remap/"
  mkdir -p $outdir

  while IFS= read -r model; do

    infiles="${vars}_${Table}_${model}_${exp}_*.nc"
    members=$( ls ${indir}${infiles} | cut -d '_' -f 6 )

    for mem in $members; do


      infile=$( ls -1  ${indir}${vars}_${Table}_${model}_${exp}_${mem}_*_*.nc)
      outfile="${outdir}${vars}_${Table}_${model}_${exp}_${mem}_global-1_201501-210012.nc"
      #echo "$infile -> $outfile"

      if [ "$vars" = "pr" ]; then
         echo "cdo -O -L remap,global_1,./wgt/${vars}_${model}_weights.nc -seldate,20150101,21001231 $infile $outfile"
      else
         echo "cdo -O -L remap,global_1,./wgt/tas_${model}_weights.nc -seldate,20150101,21001231 $infile $outfile"
      fi
 
    done


  done < CMIP6_modellist.txt

done
