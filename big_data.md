# Big Data - Mapping a Square-Mile Grid of the U.S. to County Data

To ensure that each square-mile of the 1792 x 2944 grid of continential U.S. takes in granular demographic information relating to that square-mile, we would need to map each square-mile to a particular county. Our goal is to create a matrix with each entry in the matrix corresponding to a county ID, that can be then mapped to specific data relating to the county (e.g. population) This information can then be used to generate matrices of $\beta$ and $\gamma$ that can be fed into the SIR epidemic model.

As of 2020, there are currently 3,143 counties and county-equivalents in the 50 states and the District of Columbia. 



To run a simulation of how the virus spreads across the US geographically, we would require creating a grid of continental U.S. For the purpose of granularity, we would like each point on this grid to represent a square mile.  

So we want to solve a set of spatio-temporal PDEs over the entire US. What kind of a grid are we looking at here? Let us do a classic engineering first order approximation and pretend the US is perfectly rectangular, 2500 miles wide horizontally and 1500 miles wide vertically. Assuming we want to work at a typical granularity of 1 mile, this means a 1501 x 2501 grid of solutions. As with typical PDE discretization methods, this means a solution array of roughly 4 million terms. Iterating over this many grid points over different time intervals with various different policies implemented requires some big computate, using some standard sparse PDE method like Jacobi iteration. We can use methods of accelerated computing, shared memory parallel processing, distributed memory parallel processing and some sort of hybrid model, and these will be further elaborated on by Royce.


Majority of current models project COVID at a statewide level or focus on large densely populated areas.
Rural communities are especially underequipped to combat this virus.
We aim to model how covid 19 will spread throughout communities large and small.
We will then model how effectiveness of various containment measures.
The ability to model virus spread and containment at a micro level will allow officials to allocate resources to best combat the virus in their community.


## Description of Parallel Application
Technical description of the parallel application, programming models, platform and infrastructure

## Use of Geospark
Description of advanced features like models/platforms not explained in class, advanced functions of modules, techniques to mitigate overheads, challenging parallelization or implementation aspects...

## Technical Description
Technical description of the software design, code baseline, dependencies, how to use the code, and system and environment needed to reproduce your tests

## Performance Evaluation
Performance evaluation (speed-up, throughput, weak and strong scaling) and discussion about overheads and optimizations done
