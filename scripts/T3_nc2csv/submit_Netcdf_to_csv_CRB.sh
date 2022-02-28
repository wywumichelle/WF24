#!/bin/bash
#SBATCH -J Job_nc2csv            # Job Name
#SBATCH -o Job_nc2csv.o%j        # Output and error file name (%j expands to jobID)
#SBATCH -e Job_nc2csv.e%j        # Output and error file name (%j expands to jobID)
#SBATCH -N 1                    # Total number of mpi tasks requested
#SBATCH -n 6                   # Total number of mpi tasks requested
#SBATCH -p normal            # Queue (partition) name -- normal, development, etc.
#SBATCH -t 02:30:00               # Run time (hh:mm:ss) - 1.5 hours
#SBATCH -A A-go3                  # Account to charge time to
source ~/installz/conda_wrappers.sh
CONDA_ACTIVATE WF24
python Netcdf_to_csv_CRB.py > Netcdf_to_csv_CRB.log
