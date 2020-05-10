# Results and Discussion

## Performance evaluation
Performance evaluation (speed-up, throughput, weak and strong scaling) and discussion about overheads and optimizations done

Speedup can be seen to increase with number of cores for both AWS and Odyssey. The increase can be attributed to the fact that we are using more threads in parallel to carry out the same task, hence less overall time is needed to carry out the same computation. However, as the number of cores becomes large, the speedup is no longer linearly increasing with number of cores used. This is because there is an associated overhead with communication and synchronization due to the creation and control of threads. As number of cores increases, problem size per core decreases, and these overheads become dominant. This explains the deviation of speedup from the linear trend.

## Challenges
Description of advanced features like models/platforms not explained in class, advanced functions of modules, techniques to mitigate overheads, challenging parallelization or implementation aspects...

## Discussion
Final discussion about goals achieved, improvements suggested, lessons learnt, future work, interesting insights…
