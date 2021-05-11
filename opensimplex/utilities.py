
from math import floor as fastFloor
from ctypes import c_int64

# try:
#    from numba import njit
#    import numba
# except ImportError:
#    def njit(func=None, **kwargs):
#        def wrapper(func):
#            return func
#        return wrapper(func)

# private static int fastFloor(double x)
#     int xi = int(x)
#     return x < xi ? xi - 1 : xi
#


def overflow(x):
    # Since normal python ints and longs can be quite humongous we have to use
    # self hack to make them be able to overflow
    return c_int64(x).value


class LatticePoint2D:
    xsv, ysv = 0, 0
    dx, dy = 0.0, 0.0

    def __init__(self, xsv, ysv):
        self.xsv, self.ysv = xsv, ysv
        ssv = float(xsv + ysv) * -0.211324865405187
        self.dx, self.dy = -xsv - ssv, -ysv - ssv


class LatticePoint3D:
    xrv, yrv, zrv = 0, 0, 0
    dxr, dyr, dzr = 0.0, 0.0, 0.0
    next_on_failure, next_on_success = None, None

    def __init__(self, xrv, yrv, zrv, lattice):
        self.dxr, self.dyr, self.dzr = -xrv + lattice * 0.5, -yrv + lattice * 0.5, -zrv + lattice * 0.5
        self.xrv, self.yrv, self.zrv = xrv + lattice * 1024, yrv + lattice * 1024, zrv + lattice * 1024


class LatticePoint4D:
    xsv, ysv, zsv, wsv = 0, 0, 0, 0
    dx, dy, dz, dw = 0.0, 0.0, 0.0, 0.0

    def __init__(self, xsv, ysv, zsv, wsv):
        self.xsv, self.ysv, self.zsv, self.wsv = xsv, ysv, zsv, wsv
        ssv = float(xsv + ysv + zsv + wsv) * -0.138196601125011
        self.dx, self.dy, self.dz, self.dw = -xsv - ssv, -ysv - ssv, -zsv - ssv, -wsv - ssv


class Grad2:
    dx, dy = 0.0, 0.0

    def __init__(self, dx, dy):
        self.dx, self.dy = dx, dy


class Grad3:
    dx, dy, dz = 0.0, 0.0, 0.0

    def __init__(self, dx, dy, dz):
        self.dx, self.dy, self.dz = dx, dy, dz


class Grad4:
    dx, dy, dz, dw = 0.0, 0.0, 0.0, 0.0

    def __init__(self, dx, dy, dz, dw):
        self.dx, self.dy, self.dz, self.dw = dx, dy, dz, dw
