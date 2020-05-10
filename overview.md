

# Overview

## Problem
The global pandemic of COVID-19 has gripped the world causing significant changes in day-to-day life for a huge number of people. With any disease, and especially ones as dangerous as this one, it is important to understand how it spreads. Many models and projections exist already, but they are mostly on a coarse national/state scale. It is difficult for local authorities to fully understand the spread in their immediate regions and hence craft carefully-tailored policies. 

## Solution
We use a mechanistic model to help better understand the spread of COVID-19. We aim to generate projections on a more granular scale than current models. This empowers regional authorities to tailor containment measures to their demographic, rather than base policies on projections that are on a larger scale.

In order to do accurately model the spread, we take a $2944\times1792$ grid approximation of the US and run the spatio-temporal SIR model (explained in detail below) at each point on the grid.

## Description of model and data 
The temporal SIR model is a common epidemiological model (https://arxiv.org/abs/2003.00122) that tracks the number of Susceptible (S), Infected (I) and Removed (R) individuals in the population. Note that R consists of both recovered and dead people. To incorporate a spatial dimension, we use the more expressive spatio-temporal version (https://www.hindawi.com/journals/ijpde/2014/186437/) described by a set of partial differential equations:

$$\begin{aligned}
\frac{\partial S}{\partial t} &= d_S \nabla^2 S - \beta SI\\
\frac{\partial I}{\partial t} &= d_I \nabla^2 I + \beta SI - \gamma I\\
\frac{\partial R}{\partial t} &= d_R \nabla^2 R + \gamma I
\end{aligned}$$

As seen, this model explicitly considers the diffusion of the infection with the Laplacian operator and hence allows for a more complex and realistic simulation. We discretize the Laplacians as follows:

$$\nabla^2 S \approx  \frac{S(x-\Delta x, y) + S(x+\Delta x,y) - 4S(x,y) +S(x,y-\Delta y) + S(x,y+\Delta y)}{\Delta x\Delta y}$$

In this model, $\beta$, $\gamma$, $d_S$, $d_I$, $d_R$ describe the transmission rate, recovery rate, susceptibilty diffusion rate, infection diffusion rate and recovery diffusion rate respectively.  While it is common in most models to consider them as fixed, in order to allow for a more granular simulation, our model considers $\beta(x,y)$, $\gamma(x,y)$, $d_S(x,y)$, $d_I(x,y)$, $d_R(x,y)$, ie we allow each parameter to be different for each grid point. This is a much more realistic description of the true underlying spread mechanism in which each local region has wildly differing characteristics. Combining these, the update steps are given by:

$$\begin{aligned}
S^{t+1}_{i,j} &= S^{t}_{i,j}  + d_{S_{i,j}}(S^t_{i + 1,j} + S^t_{i - 1,j} - 4 S^t_{i ,j} + S^t_{i ,j+1} + S^t_{i ,j-1})- \beta_{i,j}S^{t}_{i,j} I^{t}_{i,j}\\
I^{t+1}_{i,j} &= I^{t}_{i,j}  + d_{I_{i,j}}(I^t_{i + 1,j} + I^t_{i - 1,j} - 4 I^t_{i ,j} + I^t_{i ,j+1} + I^t_{i ,j-1})+\beta_{i,j}S^{t}_{i,j} I^{t}_{i,j}-\gamma_{i,j}I^{t}_{i,j}\\
R^{t+1}_{i,j} &= R^{t}_{i,j}  + d_{R_{i,j}}(R^t_{i + 1,j} + R^t_{i - 1,j} - 4 R^t_{i ,j} + R^t_{i ,j+1} + R^t_{i ,j-1})+\gamma_{i,j}I^{t}_{i,j}
\end{aligned}$$

Hence, in this model, for each time step at each grid point, we will be reading in spatial information for $\beta$, $\gamma$, $d_S$, $d_I$, $d_R$ and computing the updates for $S$, $I$ and $R$. We will do this for $2944\times1792 =  5, 275,648$ grid points per time step. This is a prime example of a problem requiring Big Compute solutions lol.
