
import numpy as np
import opensimplex as simplex

default_num = 100000


class Benchmark:
    def __init__(self):
        # Randomized coordinate arrays that will supply the noise funcs.
        self.x = np.random.random_sample(default_num)
        self.y = np.random.random_sample(default_num)
        self.z = np.random.random_sample(default_num)
        self.w = np.random.random_sample(default_num)

    def run(self):
        # This is the simplest way of generating a small amount of noise values.
        # for i in range(default_num):
        #	self.simplex.noise2d(self.x[i], self.y[i])
        #	self.simplex.noise3d(self.x[i], self.y[i], self.z[i])
        #	self.simplex.noise4d(self.x[i], self.y[i], self.z[i], self.w[i])

        # The most performant way of generating a large number of noise values is by
        # creating a numpy array with your coordinates and use these versions of the
        # noise funcs, as they are optimized for arrays.
        simplex.noise2array(self.x, self.y)
        simplex.noise3array(self.x, self.y, self.z)
        simplex.noise4array(self.x, self.y, self.z, self.w)

################################################################################


if __name__ == "__main__":
    import cProfile
    b = Benchmark()
    cProfile.run("b.run()", sort="tottime")
