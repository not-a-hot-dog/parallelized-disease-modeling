# Parallelized COVID-19 Modeling

## Instructions on using the simulation tools

### OpenMP version with county data (Recommended, requires OpenMP and data download)
1. Use this [link](https://drive.google.com/file/d/1-iOfdYB9nqvazSthgwOlMHEa5q0RyXbn/view?fbclid=IwAR3xFKPT26JkwBLH0oB7WesWrTytM7ir1t9cjrPa3njt8zsip6nxq4BdmaU) and download `matrix.npy` into the `data/` subdirectory.
2. Run `python generate_data.py` to create the required data CSVs that will be placed in the `data/` subdirectory.
3. In `models/`, run `gcc -fopenmp sir_data_omp.c -o sir_data_omp` to compile the simulation code (note that this requires OpenMP; for non-OpenMP versions of the code, see below). Execute with `./sir_data_omp 10 ../results/output` to run the simulation for 10 timesteps and save the output.
4. Run `python generate_plot.py` from the main directory to create a visualization of the simulation result as `results/output.png`.

### Non-OpenMP version with county data (Requires data download)
1. Use this [link](https://drive.google.com/file/d/1-iOfdYB9nqvazSthgwOlMHEa5q0RyXbn/view?fbclid=IwAR3xFKPT26JkwBLH0oB7WesWrTytM7ir1t9cjrPa3njt8zsip6nxq4BdmaU) and download `matrix.npy` into the `data/` subdirectory.
2. Run `python generate_data.py` to create the required data CSVs that will be placed in the `data/` subdirectory.
3. In `models/`, run `gcc -DUSE_CLOCK sir_data.c timing.c -o sir_data` to compile the simulation code. Execute with `./sir_data 10 ../results/output` to run the simulation for 10 timesteps and save the output.
4. Run `python generate_plot.py` from the main directory to create a visualization of the simulation result as `results/output.png`.

### OpenMP version without county data (Requires OpenMP)
1. In `models/`, run `gcc -fopenmp sir_omp.c -o sir_omp` to compile the simulation code (note that this requires OpenMP; for non-OpenMP versions of the code, see below). Execute with `./sir_omp 10 ../results/output` to run the simulation for 10 timesteps and save the output.
4. Run `python generate_plot.py` from the main directory to create a visualization of the simulation result as `results/output.png`.

### Non-OpenMP version without county data
1. In `models/`, run `gcc -DUSE_CLOCK sir.c timing.c -o sir` to compile the simulation code. Execute with `./sir 10 ../results/output` to run the simulation for 10 timesteps and save the output.
4. Run `python generate_plot.py` from the main directory to create a visualization of the simulation result as `results/output.png`.
