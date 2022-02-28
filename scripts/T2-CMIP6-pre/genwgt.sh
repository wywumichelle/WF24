#!/bin/bash
#SBATCH -J cdo_genwgt           # job name
#SBATCH -o cdo_genwgt.o%j        # output and error file name (%j expands to jobID)
#SBATCH -N 2               # number of nodes requested
#SBATCH -n 48              # total number of mpi tasks requested
#SBATCH -p normal     # queue (partition) -- normal, development, etc.
#SBATCH -t 00:20:00         # run time (hh:mm:ss) - 1.5 hours
#SBATCH -A A-go3

#===================
# This is the script to generate the interpolations weights, 
# , and to save time while interpolating.
# Run this script befire running sel-remap.sh
# WYW, 2021
#==================


exp="ssp126"
mkdir wgt
for vars in tas pr ; do

  indir="$SCRATCH/CMIP6/mon/${exp}_${vars}/combine/"
  outdir="$SCRATCH/CMIP6/mon/${exp}_${vars}/seldate-remap/"
  mkdir -p $outdir

  while IFS= read -r model; do

    infiles="${vars}_Amon_${model}_${exp}_*.nc"
    infile=$( ls ${indir}${infiles} | sed -n '1p' )
    outfile="./wgt/${vars}_${model}_weights.nc"

    echo "$infile -> $outfile"

    if [ $vars = "pr" ]; then

      cdo -O -L gennn,global_1 $infile $outfile
 
    else

      cdo -O -L genbil,global_1 $infile $outfile

    fi
 

  done < CMIP6_modellist.txt

done
