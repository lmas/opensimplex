
import sys

from opensimplex import OpenSimplex

if sys.version_info[0] < 3:
    _range = xrange
else:
    _range = range

class Benchmark:
    def __init__(self):
        self.simplex = OpenSimplex(seed=0)

    def run(self, number=100000):
        for i in _range(number):
            self.simplex.noise2d(0.1, 0.1)
            self.simplex.noise3d(0.1, 0.1, 0.1)
            self.simplex.noise4d(0.1, 0.1, 0.1, 0.1)

if __name__ == "__main__":
    import cProfile
    b = Benchmark()
    cProfile.run("b.run()", sort="tottime")
