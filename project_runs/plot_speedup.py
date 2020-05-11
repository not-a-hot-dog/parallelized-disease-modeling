from matplotlib import pyplot as plt
import numpy as np
import os

if __name__ == '__main__':
    cores = []
    time = []
    for d in os.listdir("./output/"):
        print(d)
        if(os.path.isdir("./output/"+d)):
            print(d)
            cores.append(int(d.split("_")[1]))
            with open("./output/{}/results.txt".format(d), 'r') as fout:
                lines = fout.readlines()
                time.append(float(lines[-2].split(" ")[-2]))
    np.save("./times.npy", time)
    np.save("./cores.npy", cores)
    #print(time)
    time = np.array(time)
    fig, ax = plt.subplots()
    ax.scatter(cores, time[0]/time, color='b', marker='s', edgecolor='k', label="Actual Speedup")
    ax.plot([0, max(cores)], [0, max(cores)], linestyle='--', label="Theoretical Speedup",
           color='#888888')
    ax.set(xlabel="Number of Cores", ylabel="Time (s)")
    plt.savefig("./speedup.png")
    plt.show()
