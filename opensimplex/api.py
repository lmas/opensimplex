from typing import Union
import time

import numpy as np
from .internals import (
    _init,
    _noise2,
    _noise3,
    _noise4,
    _noise2a,
    _noise3a,
    _noise4a,
    _looping_animated_2D_image,
    _looping_animated_closed_1D_curve,
    _tileable_2D_image,
)

try:
    from numba_progress import ProgressBar
except ImportError:
    ProgressBar = None

# Why 3 (and not just 0 or something)? I ran into a bug with"overflowing int" errors while refactoring in numpy and
# using a non-zero seed value... This is a reminder
DEFAULT_SEED = 3

"""
OpenSimplex n-dimensional gradient noise algorithm, based on work by Kurt Spencer.
"""


def seed(seed: int = DEFAULT_SEED) -> None:
    """
    Seeds the underlying permutation array (which produces different outputs),
    using a 64-bit integer number.
    If no value is provided, a static default will be used instead.

    >>> seed(13)
    """
    global _default
    _default = OpenSimplex(seed)


def random_seed() -> None:
    """
    Works just like seed(), except it uses the system time (in ns) as a seed value.
    Not guaranteed to be random so use at your own risk.

    >>> random_seed()
    """
    seed(time.time_ns())


def noise2(x: float, y: float) -> float:
    """
    Generate 2D OpenSimplex noise from X,Y coordinates.
    :param x: x coordinate as float
    :param y: y coordinate as float
    :return:  generated 2D noise as float, between -1.0 and 1.0

    >>> noise2(0.5, 0.5)
    -0.43906247097569345
    """
    return _default.noise2(x, y)


def noise2array(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
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
    """
    return _default.noise2array(x, y)


def noise3(x: float, y: float, z: float) -> float:
    """
    Generate 3D OpenSimplex noise from X,Y,Z coordinates.
    :param x: x coordinate as float
    :param y: y coordinate as float
    :param z: z coordinate as float
    :return:  generated 3D noise as float, between -1.0 and 1.0

    >>> noise3(0.5, 0.5, 0.5)
    0.39504955501618155
    """
    return _default.noise3(x, y, z)


def noise3array(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """
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
    """
    return _default.noise3array(x, y, z)


def noise4(x: float, y: float, z: float, w: float) -> float:
    """
    Generate 4D OpenSimplex noise from X,Y,Z,W coordinates.
    :param x: x coordinate as float
    :param y: y coordinate as float
    :param z: z coordinate as float
    :param w: w coordinate as float
    :return:  generated 4D noise as float, between -1.0 and 1.0

    >>> noise4(0.5, 0.5, 0.5, 0.5)
    0.04520359600370195
    """
    return _default.noise4(x, y, z, w)


def noise4array(x: np.ndarray, y: np.ndarray, z: np.ndarray, w: np.ndarray) -> np.ndarray:
    """
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
    """
    return _default.noise4array(x, y, z, w)


"""
Higher-level OpenSimplex noise functions by Dennis van Gils.

Inspired by [Coding Challenge #136.1: Polar Perlin Noise Loops]
(https://www.youtube.com/watch?v=ZI1dmHv3MeM) from [The Coding Train]
(https://www.youtube.com/c/TheCodingTrain).
"""


def progress_bar_wrapper(
    noise_fun: callable,
    noise_kwargs: list,
    verbose: bool = True,
    total: int = 1,
):
    if verbose:
        print(f"{'Generating noise...':30s}")
        tick = time.perf_counter()

    if (ProgressBar is None) or (not verbose):
        out = noise_fun(**noise_kwargs)
    else:
        with ProgressBar(total=total, dynamic_ncols=True) as numba_progress:
            out = noise_fun(**noise_kwargs, progress_hook=numba_progress)

    if verbose:
        print(f"done in {(time.perf_counter() - tick):.2f} s")

    return out


def looping_animated_2D_image(
    N_frames: int = 200,
    N_pixels_x: int = 1000,
    N_pixels_y: Union[int, None] = None,
    t_step: float = 0.1,
    x_step: float = 0.01,
    y_step: Union[float, None] = None,
    dtype: type = np.double,
    seed: int = DEFAULT_SEED,
    verbose: bool = True,
) -> np.ndarray:
    """Generates a stack of seamlessly-looping animated 2D images drawn from
    OpenSimplex noise.

    The algorithm uses OpenSimplex noise in 4 dimensions. The first two
    dimensions are used to describe a plane in space, which gets projected onto
    the 2D image. The last two dimensions are used to describe a circle in
    time.

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
    :param dtype:      Return type of the noise array elements. To reduce the
                       memory footprint one can change from the default
                       `numpy.double` to e.g. `numpy.float32`.
                       (type, default=numpy.double)
    :param seed:       Seed value of the OpenSimplex noise (int, default=3)
    :param verbose:    Print 'Generating noise...' to the terminal? If the
                       `numba` and `numba_progress` packages are found a
                       progress bar will also be shown.
                       (bool, default=True)
    :return: The 2D image stack as 3D array [time, y-pixel, x-pixel] containing
             the OpenSimplex noise values as floating points. The output is
             garantueed to be in the range [-1, 1], but the exact extrema cannot
             be known a-priori and are probably quite smaller than [-1, 1].
    """

    perm, _ = _init(seed)

    out = progress_bar_wrapper(
        noise_fun=_looping_animated_2D_image,
        noise_kwargs={
            "N_frames": N_frames,
            "N_pixels_x": N_pixels_x,
            "N_pixels_y": N_pixels_y if N_pixels_y is not None else N_pixels_x,
            "t_step": t_step,
            "x_step": x_step,
            "y_step": y_step if y_step is not None else x_step,
            "dtype": dtype,
            "perm": perm,
        },
        verbose=verbose,
        total=N_frames,
    )

    return out


def looping_animated_closed_1D_curve(
    N_frames: int = 200,
    N_pixels_x: int = 1000,
    t_step: float = 0.1,
    x_step: float = 0.01,
    dtype: type = np.double,
    seed: int = DEFAULT_SEED,
    verbose: bool = True,
) -> np.ndarray:
    """Generates a stack of seamlessly-looping animated 1D curves, each curve in
    turn also closing up seamlessly back-to-front, all drawn from OpenSimplex
    noise.

    The algorithm uses OpenSimplex noise in 4 dimensions. The first two
    dimensions are used to describe a circle in space, which gets projected onto
    the 1D curve. The last two dimensions are used to describe a circle in time.

    :param N_frames:   Number of time frames (int, default=200)
    :param N_pixels_x: Number of pixels of the curve (int, default=1000)
    :param t_step:     Time step (float, default=0.1)
    :param x_step:     Spatial step in the x-direction (float, default=0.01)
    :param dtype:      Return type of the noise array elements. To reduce the
                       memory footprint one can change from the default
                       `numpy.double` to e.g. `numpy.float32`.
                       (type, default=numpy.double)
    :param seed:       Seed value of the OpenSimplex noise (int, default=3)
    :param verbose:    Print 'Generating noise...' to the terminal? If the
                       `numba` and `numba_progress` packages are found a
                       progress bar will also be shown.
                       (bool, default=True)
    :return: The 1D curve stack as 2D array [time, x-pixel] containing
             the OpenSimplex noise values as floating points. The output is
             garantueed to be in the range [-1, 1], but the exact extrema cannot
             be known a-priori and are probably quite smaller than [-1, 1].
    """

    perm, _ = _init(seed)  # The OpenSimplex seed table

    out = progress_bar_wrapper(
        noise_fun=_looping_animated_closed_1D_curve,
        noise_kwargs={
            "N_frames": N_frames,
            "N_pixels_x": N_pixels_x,
            "t_step": t_step,
            "x_step": x_step,
            "dtype": dtype,
            "perm": perm,
        },
        verbose=verbose,
        total=N_frames,
    )

    return out


def tileable_2D_image(
    N_pixels_x: int = 1000,
    N_pixels_y: Union[int, None] = None,
    x_step: float = 0.01,
    y_step: Union[float, None] = None,
    dtype: type = np.double,
    seed: int = DEFAULT_SEED,
    verbose: bool = True,
) -> np.ndarray:
    """Generates a seamlessly-tileable 2D image drawn from OpenSimplex noise.

    The algorithm uses OpenSimplex noise in 4 dimensions. The first two
    dimensions are used to describe a circle in space, which gets projected onto
    the x-axis of the 2D image. The last two dimensions are used to describe
    another circle in space, which gets projected onto the y-axis of the 2D
    image.

    :param N_pixels_x: Number of pixels on the x-axis (int, default=1000)
    :param N_pixels_y: Number of pixels on the y-axis. When set to None
                       `N_pixels_y` will be set equal to `N_pixels_x`.
                       (int | None, default=None)
    :param x_step:     Spatial step in the x-direction (float, default=0.01)
    :param y_step:     Spatial step in the y-direction. When set to None
                       `y_step` will be set equal to `x_step`.
                       (float | None, default=None)
    :param dtype:      Return type of the noise array elements. To reduce the
                       memory footprint one can change from the default
                       `numpy.double` to e.g. `numpy.float32`.
                       (type, default=numpy.double)
    :param seed:       Seed value of the OpenSimplex noise (int, default=3)
    :param verbose:    Print 'Generating noise...' to the terminal? If the
                       `numba` and `numba_progress` packages are found a
                       progress bar will also be shown.
                       (bool, default=True)
    :return: The 2D image stack as 3D array [time, y-pixel, x-pixel] containing
             the OpenSimplex noise values as floating points. The output is
             garantueed to be in the range [-1, 1], but the exact extrema cannot
             be known a-priori and are probably quite smaller than [-1, 1].
    """

    perm, _ = _init(seed)

    out = progress_bar_wrapper(
        noise_fun=_tileable_2D_image,
        noise_kwargs={
            "N_pixels_x": N_pixels_x,
            "N_pixels_y": N_pixels_y if N_pixels_y is not None else N_pixels_x,
            "x_step": x_step,
            "y_step": y_step if y_step is not None else x_step,
            "dtype": dtype,
            "perm": perm,
        },
        verbose=verbose,
        total=N_pixels_y,
    )

    return out


################################################################################

# This class is provided for backwards compatibility and might disappear in the future. Use at your own risk.
class OpenSimplex(object):
    def __init__(self, seed: int) -> None:
        self._perm, self._perm_grad_index3 = _init(seed)

    def noise2(self, x: float, y: float) -> float:
        return _noise2(x, y, self._perm)

    def noise2array(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return _noise2a(x, y, self._perm)

    def noise3(self, x: float, y: float, z: float) -> float:
        return _noise3(x, y, z, self._perm, self._perm_grad_index3)

    def noise3array(self, x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
        return _noise3a(x, y, z, self._perm, self._perm_grad_index3)

    def noise4(self, x: float, y: float, z: float, w: float) -> float:
        return _noise4(x, y, z, w, self._perm)

    def noise4array(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, w: np.ndarray) -> np.ndarray:
        return _noise4a(x, y, z, w, self._perm)


_default = OpenSimplex(DEFAULT_SEED)
