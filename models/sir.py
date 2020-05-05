import numpy as np
import matplotlib.pyplot as plt

def SIR_spatio_temporal_simulate(params):
    
    def forward_euler_spatial(current, beta, gamma, dS, dI, dR, Xmax, Ymax):
        '''Implement simple forward Euler ODE solving
        with spatial diffusion terms.'''

        S_current, I_current, R_current = current
        
        S_next = np.empty(S_current.shape)
        I_next = np.empty(I_current.shape)
        R_next = np.empty(R_current.shape)

        for i in range(1, Xmax-1):
            for j in range(1, Ymax-1):
                S_next[i,j] = S_current[i,j] - beta*S_current[i,j]*I_current[i,j] + \
                    dS * (S_current[i+1, j] + S_current[i-1, j] - 4*S_current[i, j] + S_current[i, j+1] + S_current[i, j-1])
                I_next[i,j] = I_current[i,j] + beta*S_current[i,j]*I_current[i,j] - gamma*I_current[i,j] + \
                    dI * (I_current[i+1, j] + I_current[i-1, j] - 4*I_current[i, j] + I_current[i, j+1] + I_current[i, j-1])
                R_next[i,j] = R_current[i,j] + gamma*I_current[i,j] + \
                    dR * (R_current[i+1, j] + R_current[i-1, j] - 4*R_current[i, j] + R_current[i, j+1] + R_current[i, j-1])

        return [S_next, I_next, R_next]
    
    #Time to simulate for, transmission rate, recovery rate
    Tmax, Xmax, Ymax = params['Tmax'], params['Xmax'], params['Ymax']
    beta, gamma, dS, dI, dR = params['beta'], params['gamma'], params['dS'], params['dI'], params['dR']
    #Initialise for t=0
    solution_current = [params['S_init'], params['I_init'], params['R_init']]

    for t in range(Tmax):
        solution_next = forward_euler_spatial(solution_current, beta, gamma, dS, dI, dR, Xmax, Ymax)
        
        fig,ax = plt.subplots(1, 3)
        ax[0].imshow(solution_next[0], cmap="coolwarm")
        ax[0].set_title('S')
        ax[1].imshow(solution_next[1], cmap="coolwarm")
        ax[1].set_title('I')
        ax[2].imshow(solution_next[2], cmap="coolwarm")
        ax[2].set_title('R')
        plt.suptitle(f'Simulation for t={t+1}')
        plt.savefig('tests/t_{:0>3d}.png'.format(t+1))

        solution_current = solution_next

######################################### SIMULATION PARAMETERS #########################################
R_init = np.zeros((10,10))
I_init = 0.01*np.ones((10,10))
# I_init[45:55, 45:55]=0.2
S_init = 1-I_init

params={
    'beta':0.2,
    'gamma':0.01,
    'S_init':S_init,
    'I_init':I_init,
    'R_init':R_init,
    'Tmax':100,
    'Xmax':10,
    'Ymax':10,
    'dS':0.0,
    'dI':0.05,
    'dR':0.0
}
######################################### SIMULATION PARAMETERS #########################################


SIR_spatio_temporal_simulate(params)