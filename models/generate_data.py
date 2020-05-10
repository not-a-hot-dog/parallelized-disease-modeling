import numpy as np

##Read in data matrix
data = np.load("data/matrix.npy")

print('Creating data...\n')
##Generate individual CSVs
S_init_data = data[:, :, 2]
I_init_data = data[:, :, 3]
R_init_data = data[:, :, 4]
isUS_data = data[:, :, 5]
#Use fixed beta and gamma for stable simulation
beta_data = 0.8 * np.ones(S_init_data.shape)
# beta_data = data[:, :, 0]*200
gamma_data = 0.01 * np.ones(S_init_data.shape)
# gamma_data = data[:, :, 1]/10
dS_data = 0.01 * np.ones(S_init_data.shape)
dI_data = 0.3 * np.ones(S_init_data.shape)
dR_data = 0.01 * np.ones(S_init_data.shape)
#Prevent diffusion at regions with no people
dS_data[isUS_data == 0] = 0
dI_data[isUS_data == 0] = 0
dR_data[isUS_data == 0] = 0

print('Saving data...\n')
np.savetxt('data/beta.csv', beta_data, delimiter=',')
np.savetxt('data/gamma.csv', gamma_data, delimiter=',')
np.savetxt('data/S_init.csv', S_init_data, delimiter=',')
np.savetxt('data/I_init.csv', I_init_data, delimiter=',')
np.savetxt('data/R_init.csv', R_init_data, delimiter=',')
np.savetxt('data/dS.csv', dS_data, delimiter=',')
np.savetxt('data/dI.csv', dI_data, delimiter=',')
np.savetxt('data/dR.csv', dR_data, delimiter=',')
np.savetxt('data/isUS.csv', isUS_data, delimiter=',')