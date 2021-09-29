#!/bin/bash
#SBATCH -J cdo_selmap           # job name
#SBATCH -o cdo_selmap.o%j        # output and error file name (%j expands to jobID)
#SBATCH -N 2               # number of nodes requested
#SBATCH -n 48              # total number of mpi tasks requested
#SBATCH -p normal      # queue (partition) -- normal, development, etc.
#SBATCH -t 04:30:00         # run time (hh:mm:ss) - 1.5 hours
#SBATCH -A A-go3

#===================
# This is the script to regrid the resolution to common 1 degree, and select 1850-2014.
# Run it after
#   combine.sh, for combine multilple time slices to one
#   genwgt.sh , for generate the interpolations weights, which saves time compared to using remapbil
# Run time is about 2 hours for 250 simulations (1980 timesteps)
# WYW, 2021 
#==================

exp="historical"
for vars in tas pr ; do

  indir="$SCRATCH/CMIP6/mon/${exp}_${vars}/combine/"
  outdir="$SCRATCH/CMIP6/mon/${exp}_${vars}/seldate-remap/"
  mkdir -p $outdir

  while IFS= read -r model; do

    infiles="${vars}_Amon_${model}_${exp}_*_*_185001-*.nc"
    members=$( ls ${indir}${infiles} | cut -d '_' -f 6 )

    for mem in $members; do


      infile=$( ls -1  ${indir}${vars}_Amon_${model}_${exp}_${mem}_*_*.nc)
      outfile="${outdir}${vars}_Amon_${model}_${exp}_${mem}_global-1_185001-201412.nc"
      echo "$infile -> $outfile"

      cdo -O -L remap,global_1,./${vars}_${model}_weights.nc -seldate,18500101,20141231 $infile $outfile

 
    done


  done < CMIP6_modellist.txt

done
