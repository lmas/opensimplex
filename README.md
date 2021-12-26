
OpenSimplex Noise
================================================================================

[![build-status](https://github.com/lmas/opensimplex/workflows/Tests/badge.svg?branch=master)](https://github.com/lmas/opensimplex/actions)
[![pypi-version](https://badge.fury.io/py/opensimplex.svg)](https://pypi.org/project/opensimplex/)

        OpenSimplex noise is an n-dimensional gradient noise function that was
        developed in order to overcome the patent-related issues surrounding
        Simplex noise, while continuing to also avoid the visually-significant
        directional artifacts characteristic of Perlin noise.

This is merely a python port of Kurt Spencer's original code (released
to the public domain) and neatly wrapped up in a package.

Status
================================================================================

The `main` branch contains the latest stable **v0.4**.

This version has been tested with **Python 3.7, 3.8, 3.9 on Linux,
MacOS and Windows**.

Updates:

- Adds a hard dependency on 'Numpy', for array optimizations aimed at heavier
  workloads.
- Adds optional dependency on 'Numba', for further speed optimizations using
  caching.
- General refactor and cleanup of the library and tests.
- **Breaking changes: API function names has been modified.**

Usage
================================================================================

**Installation:**

        pip install opensimplex

**Basic usage:**

        >>> import opensimplex
        >>> opensimplex.seed(1234)
        >>> n = opensimplex.noise2(x=10, y=10)
        >>> print(n)
        0.580279369186297

For more advanced examples, see the files in the `tests` and `example` directory.

**Available functions:**

*opensimplex.seed(seed)*
> Seeds the underlying permutation array (which produces different outputs),
> using a 64-bit seed number.

*opensimplex.noise2(x, y)*
> Generate 2D OpenSimplex noise from X,Y coordinates.

*opensimplex.noise2array(x, y)*
> Same as noise2, but works with numpy arrays for better performance.

*opensimplex.noise3(x, y, z)*
> Generate 3D OpenSimplex noise from X,Y,Z coordinates.

*opensimplex.noise3array(x, y, z)*
> Same as noise3, but works with numpy arrays for better performance.

*opensimplex.noise4(x, y, z, w)*
> Generate 4D OpenSimplex noise from X,Y,Z,W coordinates.

*opensimplex.noise4array(x, y, z, w)*
> Same as noise4, but works with numpy arrays for better performance.

**Running tests and benchmarks:**

        virtualenv venv
        source venv/bin/activate
        make deps

and then simply run the tests:

        make test

or the benchmark:

        make benchmark

FAQ
================================================================================

- Is this relevantly different enough to avoid any real trouble with the
original patent?

    > If you read the [patent
    > claims](http://www.google.com/patents/US6867776):
    >
    > Claim #1 talks about the hardware-implementation-optimized
    > gradient generator. Most software implementations of Simplex Noise
    > don't use this anyway, and OpenSimplex Noise certainly doesn't.
    >
    > Claim #2(&3&4) talk about using (x',y',z')=(x+s,y+s,z+s) where
    > s=(x+y+z)/3 to transform the input (render space) coordinate onto
    > a simplical grid, with the intention to make all of the
    > "scissor-simplices" approximately regular. OpenSimplex Noise (in
    > 3D) uses s=-(x+y+z)/6 to transform the input point to a point on
    > the Simplectic honeycomb lattice so that the simplices bounding
    > the (hyper)cubes at (0,0,..,0) and (1,1,...,1) work out to be
    > regular. It then mathematically works out that s=(x+y+z)/3 is
    > needed for the inverse transform, but that's performing a
    > different (and opposite) function.
    >
    > Claim #5(&6) are specific to the scissor-simplex lattice. Simplex
    > Noise divides the (squashed) n-dimensional (hyper)cube into n!
    > simplices based on ordered edge traversals, whereas OpenSimplex
    > Noise divides the (stretched) n-dimensional (hyper)cube into n
    > polytopes (simplices, rectified simplices, birectified simplices,
    > etc.) based on the separation (hyper)planes at integer values of
    > (x'+y'+z'+...).
    >
    > Another interesting point is that, if you read all of the claims,
    > none of them appear to apply to the 2D analogue of Simplex noise
    > so long as it uses a gradient generator separate from the one
    > described in claim #1. The skew function in Claim #2 only
    > applies to 3D, and #5 explicitly refers to n>=3.
    >
    > And none of the patent claims speak about using surflets /
    > "spherically symmetric kernels" to generate the "images with
    > texture that do not have visible grid artifacts," which is
    > probably the biggest similarity between the two algorithms.
    >
    > - **Kurt**, on [Reddit](https://www.reddit.com/r/proceduralgeneration/comments/2gu3e7/like_perlins_simplex_noise_but_dont_like_the/ckmqz2y)

Credits
================================================================================

- Kurt Spencer - Original work
- Alex - Python port and package author

- CreamyCookie - Cleanup and optimizations
- Owen Raccuglia - Test cases
- /u/redblobgames - Fixed conversion for Java's long type, see [Reddit](https://old.reddit.com/r/proceduralgeneration/comments/327zkm/repeated_patterns_in_opensimplex_python_port/cq8tth7/)
- PetyaVasya - Found bug with using c_long on Windows systems, see [Issue #7](https://github.com/lmas/opensimplex/issues/7)
- ktritz - First numba/numpy implementation, see [Issue #4](https://github.com/lmas/opensimplex/issues/4)
- Thomas Rometsch and MightyBOBcnc - Numba optimization tricks, see [Issue #4](https://github.com/lmas/opensimplex/issues/4)

License
================================================================================

While the original work was released to the public domain by Kurt, this
package is using the MIT license. Please see the file LICENSE for
details.

Expected Output
================================================================================

Example images visualising 2D, 3D and 4D noise on a 2D plane, using the default seed:

**2D noise**

![image](images/noise2d.png)

**3D noise**

![image](images/noise3d.png)

**4D noise**

![image](images/noise4d.png)
