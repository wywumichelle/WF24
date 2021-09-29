#!/bin/bash
#SBATCH -J cdo_ensmean           # job name
#SBATCH -o cdo_ensmean.o%j        # output and error file name (%j expands to jobID)
#SBATCH -N 2              # number of nodes requested
#SBATCH -n 48              # total number of mpi tasks requested
#SBATCH -p normal     # queue (partition) -- normal, development, etc.
#SBATCH -t 02:00:00         # run time (hh:mm:ss) - 1.5 hours
#SBATCH -A A-go3
sbatch --dependency=afterok:8501179
#===================
# This sript is to do the ensemble average into one.
# Run time depends on the number of ensembles, and the size of the files.
# 5 minutes for 3 models (1980 timesteps)
# WYW, 2021
#==================


exp="historical"

for vars in tas pr ; do

  indir="$SCRATCH/CMIP6/mon/${exp}_${vars}/seldate-remap/"
  outdir="$SCRATCH/CMIP6/mon/${exp}_${vars}/ensmean/"
  mkdir -p $outdir

  while IFS= read -r model; do
    
    infiles="${vars}_Amon_${model}_${exp}_*_global-1_185001-201412.nc"
    numf=$( ls ${indir}${infiles} | wc -l )

    if [ $numf -gt 1 ]
    then
      
      outfile="${vars}_Amon_${model}_${exp}_${numf}ensmean_global-1_185001-201412.nc"
      echo "do cdo ensmean for" ${model}_${exp}
      cdo -O ensmean ${indir}${infiles} ${outdir}${outfile}

    else

      outfile="${vars}_Amon_${model}_${exp}_1ens_global-1_185001-201412.nc"
      echo "cp " ${indir}${infiles} ${outdir}${outfile}
      cp ${indir}${infiles} ${outdir}${outfile}

    fi


  done < CMIP6_modellist.txt
done
