from .constants import np
from .internals import _init, _noise2, _noise3, _noise4, _noise2a, _noise3a, _noise4a
import time

# Why 3 (and not just 0 or something)? I ran into a bug with"overflowing int" errors while refactoring in numpy and
# using a nonzero seed value... This is a reminder
DEFAULT_SEED = 3

"""
OpenSimplex n-dimensional gradient noise algorithm,
based on work by Kurt Spencer.
"""


def seed(seed: int = DEFAULT_SEED) -> None:
    """
    Seeds the underlying permutation array (which produces different outputs),
    using a 64-bit seed number.
    """
    global _default
    _default = OpenSimplex(seed)


def random_seed() -> None:
    """
    Works just like seed(), except it uses the system time (in ns) as a seed value.
    Not guaranteed to be random so use at your own risk.
    """
    seed(time.time_ns())


def noise2(x: float, y: float) -> float:
    """
    Generate 2D OpenSimplex noise from X,Y coordinates.
    """
    return _default.noise2(x, y)


def noise2array(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Generates 2D OpenSimplex noise using Numpy arrays for increased performance.
    :param x: numpy array of x-coords
    :param y: numpy array of y-coords
    :return: 2D numpy array of shape (y.size, x.size) with the generated noise for the supplied coordinates.
    """
    return _default.noise2array(x, y)


def noise3(x: float, y: float, z: float) -> float:
    """
    Generate 3D OpenSimplex noise from X,Y,Z coordinates.
    """
    return _default.noise3(x, y, z)


def noise3array(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """
    Generates 3D OpenSimplex noise using Numpy arrays for increased performance.
    :param x: numpy array of x-coords
    :param y: numpy array of y-coords
    :param z: numpy array of z-coords
    :return: 3D numpy array of shape (z.size, y.size, x.size) with the generated noise for the supplied coordinates.
    """
    return _default.noise3array(x, y, z)


def noise4(x: float, y: float, z: float, w: float) -> float:
    """
    Generate 4D OpenSimplex noise from X,Y,Z,W coordinates.
    """
    return _default.noise4(x, y, z, w)


def noise4array(x: np.ndarray, y: np.ndarray, z: np.ndarray, w: np.ndarray) -> np.ndarray:
    """
    Generates 4D OpenSimplex noise using Numpy arrays for increased performance.
    :param x: numpy array of x-coords
    :param y: numpy array of y-coords
    :param z: numpy array of z-coords
    :param w: numpy array of w-coords
    :return: 4D numpy array of shape (w.size, z.size, y.size, x.size) with the generated noise for the supplied
    coordinates.
    """
    return _default.noise4array(x, y, z, w)


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
