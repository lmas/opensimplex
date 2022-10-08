
# OpenSimplex Noise

[![build-status](https://github.com/lmas/opensimplex/workflows/Tests/badge.svg?branch=master)](https://github.com/lmas/opensimplex/actions)
[![pypi-version](https://img.shields.io/pypi/v/opensimplex?label=Version)](https://pypi.org/project/opensimplex/)
[![pypi-downloads](https://img.shields.io/pypi/dm/opensimplex?label=Downloads)](https://pypistats.org/packages/opensimplex)

[OpenSimplex] is a noise generation function like [Perlin] or [Simplex] noise, but better.

    OpenSimplex noise is an n-dimensional gradient noise function that was
    developed in order to overcome the patent-related issues surrounding
    Simplex noise, while continuing to also avoid the visually-significant
    directional artifacts characteristic of Perlin noise.
    - Kurt Spencer

This is merely a python port of Kurt Spencer's [original code] (released to the public domain)
and neatly wrapped up in a package.

[OpenSimplex]: https://en.wikipedia.org/wiki/OpenSimplex_noise
[Perlin]: https://en.wikipedia.org/wiki/Perlin_noise
[Simplex]: https://en.wikipedia.org/wiki/Simplex_noise
[original code]: https://gist.github.com/KdotJPG/b1270127455a94ac5d19

## Status

The `master` branch contains the latest code (possibly unstable),
with automatic tests running for **Python 3.8, 3.9, 3.10 on Linux, MacOS and Windows**.

Please refer to the [version tags] for the latest stable version.

[version tags]: https://github.com/lmas/opensimplex/tags


Updates for **v0.4+**:

- Adds a hard dependency on 'Numpy', for array optimizations aimed at heavier workloads.
- Adds optional dependency on 'Numba', for further speed optimizations using caching
  (currently untested due to issues with llvmlite).
- Adds typing support.
- General refactor and cleanup of the library, tests and docs.
- **Breaking changes: API functions uses new names.**

## Usage

**Installation**

    pip install opensimplex

**Basic usage**

    >>> import opensimplex
    >>> opensimplex.seed(1234)
    >>> n = opensimplex.noise2(x=10, y=10)
    >>> print(n)
    0.580279369186297

**Running tests and benchmarks**

Setup a development environment:

    make dev
    source devenv/bin/activate
    make deps

And then run the tests:

    make test

Or the benchmarks:

    make benchmark

For more advanced examples, see the files in the [tests](./tests/) and [examples](./examples/) directories.

## API

**opensimplex.seed(seed)**

    Seeds the underlying permutation array (which produces different outputs),
    using a 64-bit integer number.
    If no value is provided, a static default will be used instead.

    seed(13)

**random_seed()**

    Works just like seed(), except it uses the system time (in ns) as a seed value.
    Not guaranteed to be random so use at your own risk.

    random_seed()

**opensimplex.noise2(x, y)**

    Generate 2D OpenSimplex noise from X,Y coordinates.
    :param x: x coordinate as float
    :param y: y coordinate as float
    :return:  generated 2D noise as float, between -1.0 and 1.0

    >>> noise2(0.5, 0.5)
    -0.43906247097569345

**opensimplex.noise2array(x, y)**

    Generates 2D OpenSimplex noise using Numpy arrays for increased performance.
    :param x: numpy array of x-coords
    :param y: numpy array of y-coords
    :return:  2D numpy array of shape (y.size, x.size) with the generated noise
              for the supplied coordinates

    >>> rng = numpy.random.default_rng(seed=0)
    >>> ix, iy = rng.random(2), rng.random(2)
    >>> noise2array(ix, iy)
    array([[ 0.00449931, -0.01807883],
           [-0.00203524, -0.02358477]])

**opensimplex.noise3(x, y, z)**

    Generate 3D OpenSimplex noise from X,Y,Z coordinates.
    :param x: x coordinate as float
    :param y: y coordinate as float
    :param z: z coordinate as float
    :return:  generated 3D noise as float, between -1.0 and 1.0

    >>> noise3(0.5, 0.5, 0.5)
    0.39504955501618155

**opensimplex.noise3array(x, y, z)**

    Generates 3D OpenSimplex noise using Numpy arrays for increased performance.
    :param x: numpy array of x-coords
    :param y: numpy array of y-coords
    :param z: numpy array of z-coords
    :return:  3D numpy array of shape (z.size, y.size, x.size) with the generated
              noise for the supplied coordinates

    >>> rng = numpy.random.default_rng(seed=0)
    >>> ix, iy, iz = rng.random(2), rng.random(2), rng.random(2)
    >>> noise3array(ix, iy, iz)
    array([[[0.54942818, 0.54382411],
            [0.54285204, 0.53698967]],
           [[0.48107672, 0.4881196 ],
            [0.45971748, 0.46684901]]])

**opensimplex.noise4(x, y, z, w)**

    Generate 4D OpenSimplex noise from X,Y,Z,W coordinates.
    :param x: x coordinate as float
    :param y: y coordinate as float
    :param z: z coordinate as float
    :param w: w coordinate as float
    :return:  generated 4D noise as float, between -1.0 and 1.0

    >>> noise4(0.5, 0.5, 0.5, 0.5)
    0.04520359600370195

**opensimplex.noise4array(x, y, z, w)**

    Generates 4D OpenSimplex noise using Numpy arrays for increased performance.
    :param x: numpy array of x-coords
    :param y: numpy array of y-coords
    :param z: numpy array of z-coords
    :param w: numpy array of w-coords
    :return:  4D numpy array of shape (w.size, z.size, y.size, x.size) with the
              generated noise for the supplied coordinates

    >>> rng = numpy.random.default_rng(seed=0)
    >>> ix, iy, iz, iw = rng.random(2), rng.random(2), rng.random(2), rng.random(2)
    >>> noise4array(ix, iy, iz, iw)
    array([[[[0.30334626, 0.29860705],
             [0.28271858, 0.27805178]],
            [[0.26601215, 0.25305428],
             [0.23387872, 0.22151356]]],
           [[[0.3392759 , 0.33585534],
             [0.3343468 , 0.33118285]],
            [[0.36930335, 0.36046537],
             [0.36360679, 0.35500328]]]])

**polar_loop_2D_stack(N_frames, N_pixels_x, N_pixels_y, t_step, x_step, y_step, seed, verbose, dtype)**

    Generates OpenSimplex noise as a stack of 2D arrays. Simply speaking, the
    stack can be seen as a set of time frames each containing a 2D pixel image
    drawn from OpenSimplex noise. Subsequent time frames hold the evolution of
    the 2D image, smoothly changing over time, also as dictated by OpenSimplex
    noise. The last frame will match up smoothly to the first frame again.

    This function can be useful for e.g. the generation of seamlessly-looping
    animated textures.

    The algorithm uses OpenSimplex noise in 4 dimensions. The first two
    dimensions are used to describe a plane in space, which get projected onto
    a 2D image. The last two dimensions are used to describe a circle in time.
    Hence the name `polar loop` as there is one circle being followed in 4D
    space.

    Note: The first frame is always identical to `noise4array(ix, iy, 0, 0)`.

    Inspiritation taken from [Coding Challenge #136.1: Polar Perlin Noise Loops]
    (https://www.youtube.com/watch?v=ZI1dmHv3MeM) by [The Coding Train]
    (https://www.youtube.com/c/TheCodingTrain).

    :param N_frames:   Number of time frames (int, default=200)
    :param N_pixels_x: Number of pixels on the x-axis (int, default=1000)
    :param N_pixels_y: Number of pixels on the y-axis. When set to None
                       `N_pixels_y` will be set equal to `N_pixels_x`.
                       (int | None, default=None)
    :param t_step:     Time step (float, default=0.1)
    :param x_step:     Spatial step in the x-direction (float, default=0.01)
    :param y_step:     Spatial step in the y-direction. When set to None
                       `y_step` will be set equal to `x_step`.
                       (float | None, default=None)
    :param seed:       Seed value of the OpenSimplex noise (int, default=3)
    :param verbose:    Print 'Generating noise...' to the terminal? If the
                       `numba` and `numba_progress` packages are found a
                       progress bar will also be shown.
                       (bool, default=True)
    :param dtype:      Return type of the noise array elements. To reduce the
                       memory footprint one can change from the default
                       `numpy.double` to e.g. `numpy.float32`.
                       (type, default=numpy.double)
    :return: The 2D image stack as 3D array [time, y-pixel, x-pixel] containing
             the OpenSimplex noise values as floating points. The output is
             garantueed to be in the range [-1, 1], but the exact extrema cannot
             be known a-priori and are probably quite smaller than [-1, 1].

**double_polar_loop_1D_stack(N_frames, N_pixels_x, t_step, x_step, seed, verbose, dtype)**

    Generates OpenSimplex noise as a stack of 1D arrays. Simply speaking, the
    stack can be seen as a set of time frames each containing an 1D pixel line
    drawn from OpenSimplex noise. The starting and ending points of each line
    are smoothly matching up. I.e., it smoothly closes back to front. Subsequent
    time frames hold the evolution of the 1D line shape, smoothly changing over
    time, also as dictated by OpenSimplex noise. The last frame will match up
    smoothly to the first frame again.

    This function can be useful for e.g. the generation of seamlessly-looping
    animated closed shapes.

    The algorithm uses OpenSimplex noise in 4 dimensions. The first two
    dimensions are used to describe a circle in space, which get projected onto
    an 1D line. The last two dimensions are used to describe a circle in time.
    Hence the name `double polar loop` as there are two circles being followed
    in 4D space.

    Inspiritation taken from [Coding Challenge #136.1: Polar Perlin Noise Loops]
    (https://www.youtube.com/watch?v=ZI1dmHv3MeM) by [The Coding Train]
    (https://www.youtube.com/c/TheCodingTrain).

    :param N_frames:   Number of time frames (int, default=200)
    :param N_pixels_x: Number of pixels on the x-axis (int, default=1000)
    :param N_pixels_y: Number of pixels on the y-axis. When set to None
                       `N_pixels_y` will be set equal to `N_pixels_x`.
                       (int | None, default=None)
    :param t_step:     Time step (float, default=0.1)
    :param x_step:     Spatial step in the x-direction (float, default=0.01)
    :param y_step:     Spatial step in the y-direction. When set to None
                       `y_step` will be set equal to `x_step`.
                       (float | None, default=None)
    :param seed:       Seed value of the OpenSimplex noise (int, default=3)
    :param verbose:    Print 'Generating noise...' to the terminal? If the
                       `numba` and `numba_progress` packages are found a
                       progress bar will also be shown.
                       (bool, default=True)
    :param dtype:      Return type of the noise array elements. To reduce the
                       memory footprint one can change from the default
                       `numpy.double` to e.g. `numpy.float32`.
                       (type, default=numpy.double)
    :return: The 1D line stack as 2D array [time, x-pixel] containing
             the OpenSimplex noise values as floating points. The output is
             garantueed to be in the range [-1, 1], but the exact extrema cannot
             be known a-priori and are probably quite smaller than [-1, 1].

## FAQ

- What does the distribution of the noise values look like?

![Noise Distribution](https://github.com/lmas/opensimplex/raw/master/images/distribution.png)

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
    > - **Kurt**, on [Reddit].

[Reddit]: https://www.reddit.com/r/proceduralgeneration/comments/2gu3e7/like_perlins_simplex_noise_but_dont_like_the/ckmqz2y


## Credits

- Kurt Spencer - Original work
- Alex - Python port and package author

- Owen Raccuglia - Test cases, [Go Module]
- /u/redblobgames - Fixed conversion for Java's long type, see [Reddit]

And all the other Github [Contributors] and [Bug Hunters]!

Thanks!

[Go Module]: https://github.com/ojrac/opensimplex-go
[Reddit]: https://old.reddit.com/r/proceduralgeneration/comments/327zkm/repeated_patterns_in_opensimplex_python_port/cq8tth7/
[Contributors]: https://github.com/lmas/opensimplex/graphs/contributors
[Bug Hunters]: https://github.com/lmas/opensimplex/issues?q=is%3Aclosed

## License

While the original work was released to the public domain by Kurt, this package is using the MIT license.

Please see the file LICENSE for details.

## Example Output

Example images visualising 2D, 3D and 4D noise on a 2D plane, using the default seed:

**2D noise**

![Noise 2D](https://github.com/lmas/opensimplex/raw/master/images/noise2d.png)

**3D noise**

![Noise 3D](https://github.com/lmas/opensimplex/raw/master/images/noise3d.png)

**4D noise**

![Noise 4D](https://github.com/lmas/opensimplex/raw/master/images/noise4d.png)

**Polar loop 2D stack**

E.g., seamlessly looping animated texture
![Polar loop 2D stack](/images/polar_loop_2D_stack.gif)

**Double polar loop 1D stack**

E.g., seamlessly looping animated closed shape
![Double polar loop 1D stack](/images/double_polar_loop_1D_stack.gif)