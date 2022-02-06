# The test samples zip were completely stolen from:
# https://github.com/ojrac/opensimplex-go/blob/master/opensimplex_test.go
# Full credits to Owen Raccuglia (ojrac).
# 2021-10-04: As of today his project was still operating under a
# "Unlicense" license, so I see no problem with stealing the samples.

import gzip
import json
import unittest
import numpy as np
import opensimplex as simplex

test_seeds = (
    # No reason for picking these seeds. They're just "big".
    (-1000000000, -0.07384566459931621),
    (0, -0.7752903093693847),
    (1000000000, 0.014494483991342916),
)


class TestOpensimplex(unittest.TestCase):
    def test_seeds(self):
        for row in test_seeds:
            simplex.seed(row[0])
            n = simplex.noise2(0.5, 0.5)
            if n != row[1]:
                self.fail("got %s, expected %s (using seed %s)" % (n, row[1], row[0]))

    def load_samples(self):
        for line in gzip.open("tests/samples.json.gz"):
            # Python3: need to decode the line as it's a bytes object and json
            # will only work on strings!
            yield json.loads(line.decode("utf-8"))

    def test_samples(self):
        simplex.seed(0)
        # Eeh ain't pretty but works for now
        samples2 = np.empty((0, 2), np.double)
        expected2 = np.empty((0), np.double)
        samples3 = np.empty((0, 3), np.double)
        expected3 = np.empty((0), np.double)
        samples4 = np.empty((0, 4), np.double)
        expected4 = np.empty((0), np.double)

        for s in self.load_samples():
            if len(s) == 3:
                expected = s[2]
                actual = simplex.noise2(s[0], s[1])
            elif len(s) == 4:
                expected = s[3]
                actual = simplex.noise3(s[0], s[1], s[2])
            elif len(s) == 5:
                expected = s[4]
                actual = simplex.noise4(s[0], s[1], s[2], s[3])
            else:
                self.fail("Unexpected sample size: " + str(len(s)))
            self.assertEqual(expected, actual)


################################################################################


if __name__ == "__main__":
    unittest.main()
