import numpy as np
import pandas as pd
import os
import sys
import socket
import subprocess
import copy
import itertools
import json

TMP_DIR = 'tmp'
TEMPLATE = 'template.sh'
OUTPUT_DIR = 'output'

def safe_zip(*args):
	if(len(args) > 0):
		first = args[0]
		for a in args[1:]:
			assert(len(a) == len(first))
	return list(zip(*args))

def submit_job(outdir, template, exp_kwargs, nn=1, nc=4, mem=1000, partition='test', time='0-0:05'):
	#print(outdir)
	#print(template)
	#print(exp_kwargs)

	exp_dir = outdir
	if(not os.path.exists(exp_dir)):
		os.mkdir(exp_dir)

	# Replace values of interest in template
	script = copy.deepcopy(template)
	script = script.replace("NN", str(nn)) # Number of nodes
	script = script.replace("NC", str(nc)) # Number of cores per node
	script = script.replace("KWARGS", str(list(exp_kwargs.values()))[1:-1])
	script = script.replace("OUTPUTDIR", str(exp_dir))
	script = script.replace('TIME', str(time))
	script = script.replace('MEM', str(mem))
	script = script.replace('PARTITION', str(partition))

	# Temporary run script
	sname = os.path.join(TMP_DIR, 'slurm_tmp.sh')
	with open(sname, 'w') as f:
		f.write(script)
	f.close()

	# Compile
	os.system('gcc -fopenmp sir_omp.c timing.c -o sir_omp')

	# Run it
	ret = subprocess.call('sbatch {}'.format(sname).split(' '))
	if(ret != 0):
		print("ERROR CODE {} WHEN SUBMITTING JOB FOR {}".format(ret, sname))


if __name__ == '__main__':
	# Parameters of SIR model
	queue = {
		'Xmax': [100],
		'Ymax': [100],
		'nsteps':[100], 
		'beta': [0.01],
		'gamma': [0.01],
		'dS': [0.01],
		'dI': [0.01],
		'dR': [0.01]
	}

    # Run parameters for job
	num_nodes = 1
	num_cores = 3
	mem = 1000                # Megabytes of memory
	partition = 'test'        # Partition to submit ti
	time = '0-0:05'           # Run time
	with open(TEMPLATE, 'r') as f:
		template = f.read()
	f.close()

	for vals in itertools.product(*list(queue.values())):
		print(vals)
		exp_kwargs = dict(safe_zip(queue.keys(), vals))
		submit_job(OUTPUT_DIR, template, exp_kwargs, num_nodes, num_cores, mem, partition, time)
	pass
