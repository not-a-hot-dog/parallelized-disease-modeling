# Results and Discussion

<p align="center">
<img src="https://raw.githubusercontent.com/not-a-hot-dog/parallelized-disease-modeling/gh-pages/_images/data_spread.gif"/>
</p>

## Performance evaluation
Performance evaluation (speed-up, throughput, weak and strong scaling) and discussion about overheads and optimizations done

Speedup can be seen to increase with number of cores for both AWS and Odyssey. The increase can be attributed to the fact that we are using more threads in parallel to carry out the same task, hence less overall time is needed to carry out the same computation. However, as the number of cores becomes large, the speedup is no longer linearly increasing with number of cores used. This is because there is an associated overhead with communication and synchronization due to the creation and control of threads. As number of cores increases, problem size per core decreases, and these overheads become dominant. This explains the deviation of speedup from the linear trend.

## Challenges
### Big Data
The initial mapping of the continental United States proved more challenging than anticipated. A simple lat-long grid with even increments doesn't work with the curvature of the earth, thus requiring us to customize a solution on how to scale the longitudes as we moved North.

Once the grid was complete we had to implement several tools not discussed in class to speed-up the mapping coordinates to county time. We had to learn how to use and implement Amazon EMR and GeoSpark to scale our data processing and generate our matrix in a timely manner.

### Big Compute

Description of advanced features like models/platforms not explained in class, advanced functions of modules, techniques to mitigate overheads, challenging parallelization or implementation aspects...

## Discussion
Final discussion about goals achieved, improvements suggested, lessons learnt, future work, interesting insights…
