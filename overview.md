# Overview

## Problem
Problem we are solving and why the need for HPC and/or Big Data
The global pandemic of COVID-19 has gripped the world causing significant changes in day-to-day life for a huge number of people.
With any disease, and especially ones as dangerous as this one, it is important to understand how it spreads.
We aim to use the SIR model to help better understand the spread of COVID-19.

In order to do accurately model the spread, we take a rough grid approximation of the US and run the SIR model at each point on the grid.
Diffusion between the grid points is used to model movement of people.
The rough US grid is a 2944x1792 matrix of populations.
Excluding cells with zero population, we have on the order of $$10^7$$ calculations to perform at every step.


## Solution
How does it compare with existing work on the problem

## Description of model and data 
Where did it come from, how did you acquire it, what does it mean, etc.

The SIR model is a basic model that tracks the number of Susceptible, Infected, and Removed people in the population.
Removed people are those that are no longer susceptible or infected, it accounts for both recovered and dead people.

