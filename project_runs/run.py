import numpy as np
import pandas as pd
import os
import sys
import socket
import subprocess
import copy
import itertools
import json


def submit_job(outdir, template, nn=1, nc=4, mem=1000, partition='test', time='0-0:05', steps=10):

    # Make output directory
    exp_dir = outdir
    if(not os.path.exists(exp_dir)):
        os.mkdir(exp_dir)

    # Replace values of interest in template
    script = copy.deepcopy(template)
    script = script.replace("NN", str(nn)) # Number of nodes
    script = script.replace("NC", str(nc)) # Number of cores per node
    script = script.replace("OUTPUTDIR", str(exp_dir))
    script = script.replace('TIME', str(time))
    script = script.replace('MEM', str(mem))
    script = script.replace('PARTITION', str(partition))
    script = script.replace("STEPS", str(steps))

    # Temporary run script
    sname = os.path.join(TMP_DIR, 'slurm_tmp_{}.sh'.format(nc))
    with open(sname, 'w') as f:
        f.write(script)
    f.close()

    # Compile
    os.system('gcc -DUSE_CLOCK -fopenmp sir_data_omp.c timing.c -o sir')

    # Run it
    ret = subprocess.call('sbatch {}'.format(sname).split(' '))
    if(ret != 0):
        print("ERROR CODE {} WHEN SUBMITTING JOB FOR {}".format(ret, sname))


if __name__ == '__main__':
    SPEEDUP = False
    TMP_DIR = 'tmp'
    TEMPLATE = 'template.sh'
    OUTPUT_DIR = 'output'

    if(not os.path.exists(OUTPUT_DIR)):
        os.mkdir(OUTPUT_DIR)

    if(not os.path.exists(TMP_DIR)):
        os.mkdir(TMP_DIR)

    # Run parameters for job
    num_nodes = 1
    num_cores = list(range(1,5))
    nc = 2
    mem = 5000                      # Megabytes of memory
    partition = 'test'              # Partition to submit ti
    time = '0-0:05'                 # Run time
    steps = 10                      # Number of steps to run
    with open(TEMPLATE, 'r') as f:  # 
        template = f.read()
    f.close()

    #for vals in itertools.product(*list(queue.values())):
    if(SPEEDUP):
        for nc in num_cores:
            print("RUNNING")
            outdir = OUTPUT_DIR + "/results_{}".format(nc)
            submit_job(outdir, template, num_nodes, nc, mem, partition, time, steps)

    else:
        outdir = '../results/'
        submit_job(outdir, template, num_nodes, nc, mem, partition, time, steps)
