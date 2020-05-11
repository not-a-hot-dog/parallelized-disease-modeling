# Parallelized COVID-19 Modeling

## Instructions for running on Odyssey

### Required Directory Structure
In order to run on the cluster, the required directory structure is shown below:

```
generate_data.py
generate_plot.py
data/
|  matrix.npy
project_runs/
|  run.py
|  sir_data_omp.c
|  template.sh
|  timing.c
|  timing.h
|  plot_speedup.py
results/
```

`matrix.npy` contains granular county-level data. Download instructions are provided below. `generate_data.py` creates the required data CSVs from `matrix.py` and stores them in `data/`. `generate_plot.py` reads in the simulation output from `results/output` and plots them in `results/output.png`. `run.py` handles compilation and setting appropriate environment variables for number of cores. Slurm job parameters such as number of nodes, cores, runtime, and partition are updated in the `__main__` section of `run.py`, as well as number of timesteps to simulate for. The rest of the files are the actual models.

### Required Dependencies
The compiler `gcc/8.2.0-fasrc1` is used. `OpenMP` comes prebuilt with the compiler. `Python 3.7.7` is used. Runs are executed on the default Odyssey operating system at the time of submission: `CentOS Linux release 7.6.1810 (Core)`.

Run `module load python/3.7.7-fasrc01` and `module load gcc/8.2.0-fasrc01` to get the required dependencies.

### Running the simulation tools
1. Use this [link](https://drive.google.com/file/d/1-iOfdYB9nqvazSthgwOlMHEa5q0RyXbn/view?fbclid=IwAR3xFKPT26JkwBLH0oB7WesWrTytM7ir1t9cjrPa3njt8zsip6nxq4BdmaU) and download `matrix.npy` into the `data/` subdirectory.
2. Run `python3 generate_data.py` (might take ~1 min) to create the required data CSVs that will be placed in the `data/` subdirectory.
3. Run `python run.py` from `project_runs/`.
4. Run `python3 generate_plot.py` from the main directory to create a visualization of the simulation result as `results/output.png`.

## Instructions for running on AWS

### Required Directory Structure
In order to run on AWS, the required directory structure is shown below:

```
generate_data.py
generate_plot.py
data/
|  matrix.npy
models/
|  sir_data_omp.c
|  sir_data.c
|  timing.c
|  timing.h
results/
```

`matrix.npy` contains granular county-level data. Download instructions are provided below. `generate_data.py` creates the required data CSVs from `matrix.py` and stores them in `data/`. `generate_plot.py` reads in the simulation output from `results/output` and plots them in `results/output.png`. The rest of the files are the actual models.

### Required Dependencies
We recommend running on an AWS t2.2xlarge instance with Ubuntu 16.04. `Python 3.5.2` was used, with `numpy` and `matplotlib`. The `gcc 5.5.0` compiler was used, with OpenMP support needed to run the OpenMP version below.

### Running the simulation tools

#### OpenMP version (Recommended, requires OpenMP and data download)
1. Use this [link](https://drive.google.com/file/d/1-iOfdYB9nqvazSthgwOlMHEa5q0RyXbn/view?fbclid=IwAR3xFKPT26JkwBLH0oB7WesWrTytM7ir1t9cjrPa3njt8zsip6nxq4BdmaU) and download `matrix.npy` into the `data/` subdirectory.
2. Run `python3 generate_data.py` (might take ~1 min) to create the required data CSVs that will be placed in the `data/` subdirectory.
3. In `models/`, run `gcc -fopenmp sir_data_omp.c -o sir_data_omp` to compile the simulation code (note that this requires OpenMP; for non-OpenMP versions of the code, see below). Execute with `./sir_data_omp 10 ../results/output` to run the simulation for 10 timesteps and save the output.
4. Run `python3 generate_plot.py` from the main directory to create a visualization of the simulation result as `results/output.png`.

#### Non-OpenMP version (Requires data download)
1. Use this [link](https://drive.google.com/file/d/1-iOfdYB9nqvazSthgwOlMHEa5q0RyXbn/view?fbclid=IwAR3xFKPT26JkwBLH0oB7WesWrTytM7ir1t9cjrPa3njt8zsip6nxq4BdmaU) and download `matrix.npy` into the `data/` subdirectory.
2. Run `python3 generate_data.py` (might take ~1 min) to create the required data CSVs that will be placed in the `data/` subdirectory.
3. In `models/`, run `gcc -DUSE_CLOCK sir_data.c timing.c -o sir_data` to compile the simulation code. Execute with `./sir_data 10 ../results/output` to run the simulation for 10 timesteps and save the output.
4. Run `python3 generate_plot.py` from the main directory to create a visualization of the simulation result as `results/output.png`.

## Instructions for running Big Data methods

Kindly refer to the README in `spark_files`.

