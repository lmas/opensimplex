
# This test was completely stolen from:
# https://github.com/ojrac/opensimplex-go/blob/master/opensimplex_test.go
# Full credits to Owen Raccuglia (ojrac).

import gzip
import json
import unittest
from opensimplex import OpenSimplex

class TestOpensimplex(unittest.TestCase):
    def load_samples(self):
        for line in gzip.open("tests/samples.json.gz"):
            # Python3: need to decode the line as it's a bytes object and json
            # will only work on strings!
            # TODO BUG: it will also take about 14 seconds to run the tests now! wtf
            yield json.loads(line.decode("utf-8"))

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
