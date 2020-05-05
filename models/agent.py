import numpy as np
import matplotlib.pyplot as plt

def agent_simulate(params):

    #Time to simulate for, transmission rate, recovery rate
    n_people, Tmax, Xmax, sigma = params['n_people'], params['Tmax'], params['Xmax'], params['sigma']
    epsilon, p = params['epsilon'], params['p']
    #Initialise for t=0
    coords = np.random.rand(n_people,2)
    infected = np.zeros(n_people)
    #Infect five people
    infected[:5] = 1

    def random_walk(current, sigma, Xmax):
        '''Simulate one time step of random walk.'''
        new = current + sigma*np.random.randn(current.shape[0], current.shape[1])
        new[new > Xmax] = Xmax
        new[new < 0] = 0
        return new
    
    def infect(current, infected, epsilon, p):
        '''Simulate infection spreading if people come closer than epsilon.'''
        for i in range(current.shape[0]):
            #Check who the infected person has come into contact with
            if infected[i] == 1:  
                for j in range(current.shape[0]):
                    #Check if person got close enough
                    if np.linalg.norm(current[i]-current[j]) < epsilon:
                        #Check if person got infected
                        if np.random.binomial(1, p) == 1:
                            infected[j] = 1

        return infected

    n_infected = [np.sum(infected)]
    for t in range(Tmax+1):
        
        plt.figure(figsize=(10,10))
        plt.scatter(coords[infected==0][:, 0], coords[infected==0][:, 1], c='b', label='Not Infected', s=50)
        plt.scatter(coords[infected==1][:, 0], coords[infected==1][:, 1], c='r', label='Infected', s=50)
        plt.title(f'Simulation for t={t}\nTotal={n_people}, Infected={np.sum(infected)}')
        plt.legend()
        plt.savefig('tests/t_{:0>3d}.png'.format(t))
        plt.close()

        coords = random_walk(coords, sigma, Xmax)
        infected = infect(coords, infected, epsilon, p)
        n_infected.append(np.sum(infected))

    plt.figure(figsize=(8,5))
    plt.plot(n_infected)
    plt.title('Number of Infected')
    plt.savefig('tests/num_infected.png')
    plt.close()

######################################### SIMULATION PARAMETERS #########################################
params={
    'Tmax':100,
    'Xmax':1,
    'sigma':0.02,
    'n_people':50,
    'epsilon':0.05,
    'p':0.5
}
######################################### SIMULATION PARAMETERS #########################################


agent_simulate(params)