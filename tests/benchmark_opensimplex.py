import numpy as np
import opensimplex as simplex

# Keep this number low, 'cuz noise4array() will, for example, generate x^4 noise values.
default_num = 20


class Benchmark:
    def __init__(self):
        # Randomized coordinate arrays that will supply the noise funcs.
        rng = np.random.default_rng(seed=0)
        self.x = rng.random(default_num)
        self.y = rng.random(default_num)
        self.z = rng.random(default_num)
        self.w = rng.random(default_num)
        simplex.seed(0)

    def run(self):
        # This is the simplest way of generating a small amount of noise values.
        # for i in range(default_num):
        # 	self.simplex.noise2d(self.x[i], self.y[i])
        # 	self.simplex.noise3d(self.x[i], self.y[i], self.z[i])
        # 	self.simplex.noise4d(self.x[i], self.y[i], self.z[i], self.w[i])

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
