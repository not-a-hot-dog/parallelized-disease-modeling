# Overview

## Problem
<p align="center">
<img src="https://raw.githubusercontent.com/not-a-hot-dog/parallelized-disease-modeling/gh-pages/_images/data_cases_total.png" alt>
<img src="https://raw.githubusercontent.com/not-a-hot-dog/parallelized-disease-modeling/gh-pages/_images/data_cases_pct.png" alt>
<em>Images generated from our matrix with data aggregated from the US Census Bureau, Johns Hopkins University and the New York Times.</em>
</p>

The global pandemic of COVID-19 has gripped the world causing significant changes in day-to-day life for a huge number of people. With any disease, and especially ones as dangerous as this one, it is important to understand how it spreads. Many models and projections exist already, but they are mostly on a coarse national/state scale. It is difficult for local authorities to fully understand the spread in their immediate regions and hence craft carefully-tailored policies. 

## Solution
We use a mechanistic model to help better understand the spread of COVID-19. We aim to generate projections on a more granular scale than current models. This empowers regional authorities to tailor containment measures to their demographic, rather than base policies on projections that are on a larger scale.

In order to accurately model the spread, we take a <i>2944&#215;1792</i> grid approximation of the US and run the spatio-temporal SIR model (explained in detail below) at each point on the grid.

## Description of model and data 
<p align="center">
<img src="https://raw.githubusercontent.com/not-a-hot-dog/parallelized-disease-modeling/gh-pages/_images/data_sir_group.png" alt>
<em>Plot of initial SIR parameters based on existing COVID-19 data.</em>
</p>

The temporal SIR model is a common epidemiological model ([Chen, et.al, 2020](https://arxiv.org/abs/2003.00122)) that tracks the number of Susceptible (S), Infected (I) and Removed (R) individuals in the population. Note that R consists of both recovered and dead people. To incorporate a spatial dimension, we use the more expressive spatio-temporal version ([Lotfi, et. al, 2014](https://www.hindawi.com/journals/ijpde/2014/186437/)) described by a set of partial differential equations:

<p align="center">
<img src="https://latex.codecogs.com/svg.latex?\frac{\partial&space;S}{\partial&space;t}=d_S\nabla^2S-\beta&space;SI" />  
<br>
<img src="https://latex.codecogs.com/svg.latex?\frac{\partial&space;I}{\partial&space;t}=d_I\nabla^2I&plus;\beta&space;SI-\gamma&space;I" />  
<br>
<img src="https://latex.codecogs.com/svg.latex?\frac{\partial&space;R}{\partial&space;t}=d_R\nabla^2R&plus;\gamma&space;I" />
</p>

As seen, this model explicitly considers the diffusion of the infection with the Laplacian operator and hence allows for a more complex and realistic simulation. We discretize the Laplacian as follows:

<p align="center">
<img src="https://latex.codecogs.com/svg.latex?\nabla^2S\approx\frac{S(x-\Delta&space;x,y)&plus;S(x&plus;\Delta&space;x,y)-4S(x,y)&plus;S(x,y-\Delta&space;y)&plus;S(x,y&plus;\Delta&space;y)}{\Delta&space;x\Delta&space;y}" />
</p>

<p align="center">
<img src="https://raw.githubusercontent.com/not-a-hot-dog/parallelized-disease-modeling/gh-pages/_images/data_beta_gamma.png" alt>
<em>Plot of beta and gamma hyperparameters based on a 14 day average of COVID-19 infection and recovery/death rates</em>
</p>

In this model, <i>&beta;, &gamma;, d<sub>S</sub>, d<sub>I</sub>, d<sub>R</sub></i> describe the transmission rate, recovery rate, susceptibilty diffusion rate, infection diffusion rate and recovery diffusion rate respectively. It is common in most models to consider them as fixed. However, in order to allow for a more granular simulation, our model considers <i>&beta;(x,y)$, &gamma;(x,y)$, $d<sub>S</sub>(x,y)$, $d<sub>I</sub>(x,y)$, $d<sub>R</sub>(x,y)$</i>, ie we allow each parameter to be different for each grid point. This is a much more realistic description of the true underlying spread mechanism in which each local region has wildly differing characteristics. This means that we need to create <i>2944&#215;1792</i> arrays for each of these parameters, which requires the complex processing of large amounts of granular data. This is a prime example of a problem requiring Big Data solutions. 

Combining the paramater discretizations, the update steps are given by:

<p align="center">
<img src="https://latex.codecogs.com/svg.latex?S^{t&plus;1}_{i,j}=S^{t}_{i,j}&plus;d_{S_{i,j}}(S^t_{i&plus;1,j}&plus;S^t_{i-1,j}-4S^t_{i,j}&plus;S^t_{i,j&plus;1}&plus;S^t_{i,j-1})-\beta_{i,j}S^{t}_{i,j}I^{t}_{i,j}" />  
<br>
<img src="https://latex.codecogs.com/svg.latex?I^{t&plus;1}_{i,j}=I^{t}_{i,j}&plus;d_{I_{i,j}}(I^t_{i&plus;1,j}&plus;I^t_{i-1,j}-4I^t_{i,j}&plus;I^t_{i,j&plus;1}&plus;I^t_{i,j-1})&plus;\beta_{i,j}S^{t}_{i,j}I^{t}_{i,j}-\gamma_{i,j}I^{t}_{i,j}" />  
<br>
<img src="https://latex.codecogs.com/svg.latex?R^{t&plus;1}_{i,j}=R^{t}_{i,j}&plus;d_{R_{i,j}}(R^t_{i&plus;1,j}&plus;R^t_{i-1,j}-4R^t_{i,j}&plus;R^t_{i,j&plus;1}&plus;R^t_{i,j-1})&plus;\gamma_{i,j}I^{t}_{i,j}" />
</p>

Hence, in this model, for each time step at each grid point, we will be reading in spatial information for <i>&beta;, &gamma;, d<sub>S</sub>, d<sub>I</sub>, d<sub>R</sub></i> and computing the updates for <i>S</i>, <i>I</i> and <i>R</i>. We will do this for <i>2944&#215;1792=5,275,648</i> grid points per time step. This is a prime example of a problem requiring Big Compute solutions.
