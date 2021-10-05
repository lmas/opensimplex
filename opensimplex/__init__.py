
__author__ = "Alex"
__version__ = 0.4

from .opensimplex import OpenSimplex

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


def noise2array(x, y):
    """
    Same as noise2, but works with numpy arrays for better performance.
    """
    return _default.noise2array(x, y)


def noise3(x, y, z):
    """
    Generate 3D OpenSimplex noise from X,Y,Z coordinates.
    """
    return _default.noise3(x, y, z)


def noise3array(x, y, z):
    """
    Same as noise3, but works with numpy arrays for better performance.
    """
    return _default.noise3array(x, y, z)


def noise4(x, y, z, w):
    """
    Generate 4D OpenSimplex noise from X,Y,Z,W coordinates.
    """
    return _default.noise4(x, y, z, w)


def noise4array(x, y, z, w):
    """
    Same as noise4, but works with numpy arrays for better performance.
    """
    return _default.noise4array(x, y, z, w)
