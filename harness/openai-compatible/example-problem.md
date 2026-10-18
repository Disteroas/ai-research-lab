# Sample mean or sample median?

I want to know whether the sample median is a better estimator of the centre of a distribution than
the sample mean, on synthetic data, in two situations:

1. **Clean data**: n = 50 independent draws from a normal distribution with mean 0 and standard
   deviation 1.
2. **Contaminated data**: the same, except that each draw is replaced, with probability 0.05, by a
   draw from a normal distribution with mean 0 and standard deviation 10.

"Better" means a lower mean squared error with respect to the true centre (0), estimated over many
repetitions. My expectation is that the mean wins on clean data and the median wins on contaminated
data, but I would like the lab to check it rather than assume it.

Constraints: plain Python 3 on a laptop, standard library only (no numpy), a few seconds of
computation in total. No real-world data.
