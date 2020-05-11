#!/bin/bash
#SBATCH -J slurm_NC
#SBATCH --account=cs205
#SBATCH --cpus-per-task NC
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH -t TIME # Runtime in D-HH:MM
#SBATCH -p PARTITION # partition
#SBATCH --mem-per-cpu=MEM # Memory pool for all cores (see also --mem-per-cpu)
#SBATCH -o OUTPUTDIR/out_%j.txt # File to which STDOUT will be written
#SBATCH -e OUTPUTDIR/err_%j.txt # File to which STDERR will be written
export SLURM_CPUS_PER_TASK=NC
export OMP_NUM_THREADS=NC
srun sir STEPS OUTPUTDIR/output > OUTPUTDIR/results.txt
