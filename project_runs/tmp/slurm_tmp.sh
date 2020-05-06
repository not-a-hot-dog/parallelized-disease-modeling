#!/bin/bash
#SBATCH -n 3 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH -t 0-0:05 # Runtime in D-HH:MM
#SBATCH -p test # partition
#SBATCH --mem=1000 # Memory pool for all cores (see also --mem-per-cpu)
#SBATCH -o output/out_%j.txt # File to which STDOUT will be written
#SBATCH -e output/err_%j.txt # File to which STDERR will be written

srun ./sir_omp 100, 100, 100, 0.01, 0.01, 0.01, 0.01, 0.01 > output/output
