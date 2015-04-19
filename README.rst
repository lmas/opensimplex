
################################################################################
OpenSimplex Noise
################################################################################
    OpenSimplex noise is an n-dimensional gradient noise function that was
    developed in order to overcome the patent-related issues surrounding
    Simplex noise, while continuing to also avoid the visually-significant
    directional artifacts characteristic of Perlin noise.

This is merely a python port of Kurt Spencer's original code, released to the
public domain, and neatly wrapped up in a package.

USAGE
================================================================================
Initialization:
--------------------------------------------------------------------------------

>>> from opensimplex import OpenSimplex
>>> tmp = OpenSimplex()
>>> print (tmp.noise2d(x=10, y=10))
0.732051569572

Optionally, the class accepts a seed value:

>>> tmp = OpenSimplex(seed=1)
>>> print (tmp.noise2d(x=10, y=10))
-0.4790979022623557

The seed must be a valid python number. It's used internally to generate some
permutation arrays, which is used for the noise generation.

If it isn't provided the class will **default to use 0 as the seed**.

Available class methods:
--------------------------------------------------------------------------------

OpenSimplex.noise2d(x, y)
    Generate 2D OpenSimplex noise from X,Y coordinates.

OpenSimplex.noise3d(x, y, z)
    Generate 3D OpenSimplex noise from X,Y,Z coordinates.

OpenSimplex.noise4d(x, y, z, w)
    Generate 4D OpenSimplex noise from X,Y,Z,W coordinates.

CREDITS
================================================================================
- Kurt Spencer - Original work
- A Svensson - Python port

LICENSE
================================================================================
Released into the public domain, please see the UNLICENSE file.

TODO
================================================================================
- add note about the patent issues
- scale down the images somehow

Expected Output
================================================================================
2D noise:

.. image:: images/noise2d.png

3D noise:

.. image:: images/noise3d.png

4D noise:

.. image:: images/noise4d.png

