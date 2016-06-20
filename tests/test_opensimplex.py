
import gzip
import json
import unittest
from opensimplex import OpenSimplex

class TestOpensimplex(unittest.TestCase):
    def load_samples(self):
        for line in gzip.open("tests/samples.json.gz"):
            yield json.loads(line)

    def test_samples(self):
        simplex = OpenSimplex(seed=0)

        for s in self.load_samples():
            if len(s) == 3:
                expected = s[2]
                actual = simplex.noise2d(s[0], s[1])
            elif len(s) == 4:
                expected = s[3]
                actual = simplex.noise3d(s[0], s[1], s[2])
            elif len(s) == 5:
                expected = s[4]
                actual = simplex.noise4d(s[0], s[1], s[2], s[3])
            else:
                self.fail("Unexpected sample size: " + str(len(s)))
            self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()
