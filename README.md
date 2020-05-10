# Parallelized COVID-19 Modeling

1. Use this [link](https://drive.google.com/file/d/1-iOfdYB9nqvazSthgwOlMHEa5q0RyXbn/view?fbclid=IwAR3xFKPT26JkwBLH0oB7WesWrTytM7ir1t9cjrPa3njt8zsip6nxq4BdmaU) to download `matrix.npy` in the local directory.
2. Run `python generate_data.py` to create the required data CSVs in the `data/` subdirectory.
3. In `models/`, run `gcc -fopenmp sir_data_omp.c -o sir_data_omp` to compile the simulation code. Execute with `./sir_data_omp 10 ../results/output` to run the simulation for 10 timesteps and save the output.
4. Run `python generate_plot.py` to create a visualization of the simulation result as `results/output.png`.
