__author__ = "Alex"
__version__ = "0.4.2"

from .opensimplex import OpenSimplex, np

_default = OpenSimplex()

"""
OpenSimplex n-dimensional gradient noise algorithm,
based on work by Kurt Spencer.
"""


def seed(seed):
    """
    Seeds the underlying permutation array (which produces different outputs),
    using a 64-bit seed number.
    """
    global _default
    _default = OpenSimplex(seed)


def noise2(x, y):
    """
    Generate 2D OpenSimplex noise from X,Y coordinates.
    """
    return _default.noise2(x, y)


def noise2array(x: np.ndarray, y: np.ndarray):
    """
    Generates 2D OpenSimplex noise using Numpy arrays for increased performance.
    :param x: numpy array of x-coords
    :param y: numpy array of y-coords
    :return: 2D numpy array of shape (y.size, x.size) with the generated noise for the supplied coordinates.
    """
    return _default.noise2array(x, y)


def noise3(x, y, z):
    """
    Generate 3D OpenSimplex noise from X,Y,Z coordinates.
    """
    return _default.noise3(x, y, z)


def noise3array(x: np.ndarray, y: np.ndarray, z: np.ndarray):
    """
    Generates 3D OpenSimplex noise using Numpy arrays for increased performance.
    :param x: numpy array of x-coords
    :param y: numpy array of y-coords
    :param z: numpy array of z-coords
    :return: 3D numpy array of shape (z.size, y.size, x.size) with the generated noise for the supplied coordinates.
    """
    return _default.noise3array(x, y, z)


def noise4(x, y, z, w):
    """
    Generate 4D OpenSimplex noise from X,Y,Z,W coordinates.
    """
    return _default.noise4(x, y, z, w)


def noise4array(x: np.ndarray, y: np.ndarray, z: np.ndarray, w: np.ndarray):
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
