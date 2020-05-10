# Overview

## Problem
The global pandemic of COVID-19 has gripped the world causing significant changes in day-to-day life for a huge number of people. With any disease, and especially ones as dangerous as this one, it is important to understand how it spreads. Many models and projections exist already, but they are mostly on a coarse national/state scale. It is difficult for local authorities to fully understand the spread in their immediate regions and hence craft carefully-tailored policies. 

## Solution
We use a mechanistic model to help better understand the spread of COVID-19. We aim to generate projections on a more granular scale than current models. This empowers regional authorities to tailor containment measures to their demographic, rather than base policies on projections that are on a larger scale.

In order to do accurately model the spread, we take a 2944x1792 grid approximation of the US and run the spatio-temporal SIR model (explained in detail below) at each point on the grid.

## Description of model and data 
Where did it come from, how did you acquire it, what does it mean, etc.

The temporal SIR model is a common epidemiological model (https://arxiv.org/abs/2003.00122) that tracks the number of Susceptible (S), Infected (I) and Removed (R) individuals in the population. Note that R consists of both recovered and dead people. To incorporate a spatial dimension, we use the more expressive spatio-temporal version described a set of partial differential equations:

$$\begin{aligned}
\frac{\partial S}{\partial t} &= d_S \nabla^2 S - \beta SI\\
\frac{\partial I}{\partial t} &= d_I \nabla^2 I + \beta SI - \gamma I\\
\frac{\partial R}{\partial t} &= d_R \nabla^2 R + \gamma I
\end{aligned}$$

