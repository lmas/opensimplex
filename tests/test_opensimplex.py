
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
                self.fail("expected %s, got %s (using seed %s)" % (n, row[1], row[0]))

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
                samples2 = np.append(samples2, [[s[0], s[1]]], axis=0)
                expected2 = np.append(expected2, s[2])
            elif len(s) == 4:
                samples3 = np.append(samples3, [[s[0], s[1], s[2]]], axis=0)
                expected3 = np.append(expected3, s[3])
            elif len(s) == 5:
                samples4 = np.append(samples4, [[s[0], s[1], s[2], s[3]]], axis=0)
                expected4 = np.append(expected4, s[4])
            else:
                self.fail("Unexpected sample size: " + str(len(s)))

        values2 = simplex.noise2array(samples2[:, 0], samples2[:, 1])
        if not np.array_equal(expected2, values2):
            self.fail("Generated noise2d doesn't match samples")
        values3 = simplex.noise3array(samples3[:, 0], samples3[:, 1], samples3[:, 2])
        if not np.array_equal(expected3, values3):
            self.fail("Generated noise3d doesn't match samples")
        values4 = simplex.noise4array(samples4[:, 0], samples4[:, 1], samples4[:, 2], samples4[:, 3])
        if not np.array_equal(expected4, values4):
            self.fail("Generated noise4d doesn't match samples")

################################################################################


if __name__ == "__main__":
    unittest.main()
