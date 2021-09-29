#!/bin/bash
#SBATCH -J cdo_combine            # job name
#SBATCH -o cdo_combine.o%j        # output and error file name (%j expands to jobID)
#SBATCH -N 1                      # number of nodes requested
#SBATCH -n 1                      # total number of mpi tasks requested
#SBATCH -p development            # queue (partition) -- normal, development, etc.
#SBATCH -t 01:00:00               # run time (hh:mm:ss) 
#SBATCH -A A-go3


#===================
# This is the script to combine files in timeslices into one
# run time: 50 minutes for 493 simulations
# WYW, 2021
#==================

exp="historical"
for vars in tas pr ; do

  indir="$SCRATCH/CMIP6/mon/${exp}_${vars}/"
  outdir="$SCRATCH/CMIP6/mon/${exp}_${vars}/combine/"
  mkdir -p $outdir

  while IFS= read -r model; do

    infiles="${vars}_Amon_${model}_${exp}*_185001-*.nc"
    members=$( ls ${indir}${infiles} | cut -d '_' -f 6 )

    for mem in $members; do

      filelist=${indir}${vars}_Amon_${model}_${exp}_${mem}*.nc
      numf=$( ls -1  ${indir}${vars}_Amon_${model}_${exp}_${mem}*.nc |wc -l)

      if [ $numf -gt 1 ]
      then
         sttyyyydd=$( ls $filelist | sed -n '1p' |cut -d '_' -f 8  |cut -d '-' -f 1 )
         endyyyydd=$( ls $filelist | sed -n '$p'| rev |cut -d '-' -f 1 |rev |cut -d '.' -f 1 )
         lev=$( ls $filelist | sed -n '1p' |cut -d '_' -f 7)
         echo "do cdo megetime for" ${vars}_${model}_${exp}_${mem}
         cdo -O mergetime $filelist ${outdir}${vars}_Amon_${model}_${exp}_${mem}_${lev}_${sttyyyydd}-${endyyyydd}.nc        
      else
         echo "cp " ${vars}_${model}_${exp}_${mem}
         cp $filelist $outdir
      fi 
      
    done


  done < CMIP6_modellist.txt
done
