import numpy as np
import matplotlib.pyplot as plt

output = np.loadtxt('results/output')
isUS_data = np.loadtxt('data/isUS.csv', delimiter=',')
sigmoid = lambda x: 1/(1+np.exp(-x))

plt.figure(figsize=(10,int(1792/2944*10)))
plt.imshow(sigmoid(output), cmap='Reds')
plt.imshow(isUS_data, cmap='gray', alpha=0.15)
plt.savefig('results/output.png')