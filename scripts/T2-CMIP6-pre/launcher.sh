#!/bin/bash
#SBATCH -J Job_launcher            # Job Name
#SBATCH -o Job_launcher.o%j        # Output and error file name (%j expands to jobID)
#SBATCH -N 2                    # Total number of mpi tasks requested
#SBATCH -n 6                   # Total number of mpi tasks requested
#SBATCH -p development              # Queue (partition) name -- normal, development, etc.
#SBATCH -t 01:00:00               # Run time (hh:mm:ss) - 1.5 hours
#SBATCH -A A-go3                  # Account to charge time to
module load launcher
#module load nco
JOB_FILE="/work/04380/wenying/stampede2/WF24/scripts/cdo_selmap.sh"
PARAMRUN="$TACC_LAUNCHER_DIR/paramrun"
export LAUNCHER_PLUGIN_DIR="$LAUNCHER_DIR/plugins"
export LAUNCHER_RMI="SLURM"
export LAUNCHER_WORKDIR="/work/04380/wenying/stampede2/WF24/scripts"
export LAUNCHER_JOB_FILE="$JOB_FILE"
export LAUNCHER_SCHED=interleaved
$PARAMRUN

