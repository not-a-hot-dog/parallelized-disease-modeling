# Big Compute

## Description of Parallel Application
OpenMP was used to parallelize computations in our model.
Loop level parallelization was done to optimize performance.
Explicit memory sharing was used for parameter matrices, as well as loop collapsing.
We compared execution using a single node on the Odyssey cluster against an AWS t2.2xlarge instance.
Odyssey was ultimately used for its superior performance.
We found sufficient speedup using one node that multiple were unnecessary.

## Technical Description
In order to run on the cluster, the required directory structure is shown below:

```
data/
|  beta.csv
|  gamma.csv
|  S_init.csv
|  I_init.csv
|  R_init.csv
|  dS.csv
|  dI.csv
|  dR.csv
project_runs/
|  run.py
|  sir_data_omp.c
|  template.sh
|  timing.c
|  timing.h
```

The compiler `gcc/8.2.0-fasrc1` is used. OpenMP comes prebuilt with the compiler.
Python 3.7.7 is used.
Runs are executed on the default Odyssey operating system at the time of submission: CentOS Linux release 7.6.1810 (Core).
Executing the model simple as running `python run.py`.
Slurm job parameters such as number of nodes, cores, runtime, and partition are updated in the `__main__` section of `run.py`.
Additionally, number of timesteps are updated in the same section.
The data matrices are generated from population and geographical data using `matrix.npy` and 

## Performance Evaluation`
We see a fantastic level of parallelization as number of cores increases using strong scaling.
No significant deviation from perfect speedup appears until approximately 15 cores are used.
Note, despite AWS speedup being comparable, AWS was approximately 50% slower for each calculation.
<p align="center">
<img src="https://raw.githubusercontent.com/not-a-hot-dog/parallelized-disease-modeling/gh-pages/_images/cluster_speedup.png" alt>
<em>Image generated from our 1792 x 2944 county matrix.</em>
</p>

The main overheads here is distribution between threads.
On Odyssey, the  overhead of using OpenMP was negligible (and even tended to be faster than single thread calculations without).
We see clearly, however, that this overhead is relatively insigificant when compared to the calculations being performed, as evidenced by the near perfect scaling until 15 cores.
