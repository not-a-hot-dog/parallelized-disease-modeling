#!/bin/bash
#SBATCH -n NC # Number of cores
#SBATCH -N NN # Ensure that all cores are on one machine
#SBATCH -t TIME # Runtime in D-HH:MM
#SBATCH -p PARTITION # partition
#SBATCH --mem=MEM # Memory pool for all cores (see also --mem-per-cpu)
#SBATCH -o OUTPUTDIR/out_%j.txt # File to which STDOUT will be written
#SBATCH -e OUTPUTDIR/err_%j.txt # File to which STDERR will be written

srun ./sir_omp KWARGS > OUTPUTDIR/output
