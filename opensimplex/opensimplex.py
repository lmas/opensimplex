#
# K.jpg's OpenSimplex 2, smooth variant ("SuperSimplex")
#
# - 2D is standard simplex, modified to support larger kernels.
#   Implemented using a lookup table.
# - 3D is "Re-oriented 8-point BCC noise" which constructs a
#   congruent BCC lattice in a much different way than usual.
# - 4D uses a naïve pregenerated lookup table, and averages out
#   to the expected performance.
#
# Multiple versions of each function are provided. See the
# documentation above each, for more info.

from .constants import *


class OpenSimplex:
    def __init__(self, seed=DEFAULT_SEED):
        self._perm = [0] * PSIZE
        self._permGrad2 = [Grad2] * PSIZE
        self._permGrad3 = [Grad3] * PSIZE
        self._permGrad4 = [Grad4] * PSIZE
        source = [0] * PSIZE
        #  for (i = 0 i < PSIZE i++)
        for i in range(0, PSIZE, 1):
            source[i] = i
        #  for (int i = PSIZE - 1 i >= 0 i--)
        for i in range(PSIZE - 1, 0, -1):
            seed = overflow(seed * 6364136223846793005 + 1442695040888963407)
            r = int((seed + 31) % (i + 1))
            if r < 0:
                r += (i + 1)
            self._perm[i] = source[r]
            self._permGrad2[i] = GRADIENTS_2D[self._perm[i]]
            self._permGrad3[i] = GRADIENTS_3D[self._perm[i]]
            self._permGrad4[i] = GRADIENTS_4D[self._perm[i]]
            source[r] = source[i]

    # 2D SuperSimplex noise, standard lattice orientation.
    def noise2(self, x, y):
        # Get points for A2* lattice
        s = 0.366025403784439 * float(x + y)
        xs, ys = x + s, y + s
        return self._noise2_base(xs, ys)

    # 3D Re-oriented 8-point BCC noise, classic orientation
    # Proper substitute for what 3D SuperSimplex "should" be,
    # in light of Forbidden Formulae.
    # Use noise3_XYBeforeZ or noise3_XZBeforeY instead, wherever appropriate.
    def noise3(self, x, y, z):
        # Re-orient the cubic lattices via rotation, to produce the expected look on cardinal planar slices.
        # If texturing objects that don't tend to have cardinal plane faces, you could even remove this.
        # Orthonormal rotation. Not a skew transform.
        r = (2.0 / 3.0) * float(x + y + z)
        xr, yr, zr = r - x, r - y, r - z
        # Evaluate both lattices to form a BCC lattice.
        return self._noise3_base(xr, yr, zr)

    # 4D SuperSimplex noise, classic lattice orientation.
    def noise4(self, x, y, z, w):
        # Get points for A4 lattice
        s = 0.309016994374947 * float(x + y + z + w)
        xs, ys, zs, ws = x + s, y + s, z + s, w + s
        return self._noise4_base(xs, ys, zs, ws)

####################################################################################################

    # 2D SuperSimplex noise base.
    # Lookup table implementation inspired by DigitalShadow.
    def _noise2_base(self, xs, ys):
        value = 0

        # Get base points and offsets
        xsb, ysb = fastFloor(xs), fastFloor(ys)
        xsi, ysi = float(xs - xsb), float(ys - ysb)

        # Index to point list
        a = int(xsi + ysi)
        index = (a << 2) | \
            int(xsi - ysi / 2 + 1 - a / 2.0) << 3 | \
            int(ysi - xsi / 2 + 1 - a / 2.0) << 4

        ssi = (xsi + ysi) * -0.211324865405187
        xi, yi = xsi + ssi, ysi + ssi

        # Point contributions
        # for (int i = 0 i < 4 i++)
        for i in range(0, 4, 1):
            c = LOOKUP_2D[index + i]
            dx, dy = xi + c.dx, yi + c.dy
            attn = 2.0 / 3.0 - dx * dx - dy * dy
            if attn <= 0:
                continue

            pxm, pym = int(xsb + c.xsv) & PMASK, int(ysb + c.ysv) & PMASK
            grad = self._permGrad2[self._perm[pxm] ^ pym]
            extrapolation = grad.dx * dx + grad.dy * dy
            attn *= attn
            value += attn * attn * extrapolation

        return value

    # Generate overlapping cubic lattices for 3D Re-oriented BCC noise.
    # Lookup table implementation inspired by DigitalShadow.
    # It was actually faster to narrow down the points in the loop itself,
    # than to build up the index with enough info to isolate 8 points.
    def _noise3_base(self, xr, yr, zr):
        # Get base and offsets inside cube of first lattice.
        xrb, yrb, zrb = fastFloor(xr), fastFloor(yr), fastFloor(zr)
        xri, yri, zri = float(xr - xrb), float(yr - yrb), float(zr - zrb)

        # Identify which octant of the cube we're in. self determines which cell
        # in the other cubic lattice we're in, and also narrows down one point on each.
        index = (int(xri + 0.5) << 0) | (int(yri + 0.5) << 1) | (int(zri + 0.5) << 2)

        # Point contributions
        value = 0.0
        c = LOOKUP_3D[index]
        #  while (c != null)
        while c is not None:
            dxr, dyr, dzr = xri + c.dxr, yri + c.dyr, zri + c.dzr
            attn = 0.75 - dxr * dxr - dyr * dyr - dzr * dzr
            if attn < 0:
                c = c.next_on_failure
                continue

            pxm, pym, pzm = (xrb + c.xrv) & PMASK, (yrb + c.yrv) & PMASK, (zrb + c.zrv) & PMASK
            grad = self._permGrad3[self._perm[self._perm[pxm] ^ pym] ^ pzm]
            extrapolation = grad.dx * dxr + grad.dy * dyr + grad.dz * dzr
            attn *= attn
            value += attn * attn * extrapolation
            c = c.next_on_success

        return value

    # 4D SuperSimplex noise, with XY and ZW forming orthogonal triangular-based planes.
    # Recommended for 3D terrain, where X and Y (or Z and W) are horizontal.
    # Recommended for noise(x, y, sin(time), cos(time)) trick.
    def _noise4_base(self, xs, ys, zs, ws):
        value = 0.0

        # Get base points and offsets
        xsb, ysb, zsb, wsb = fastFloor(xs), fastFloor(ys), fastFloor(zs), fastFloor(ws)
        xsi, ysi, zsi, wsi = float(xs - xsb), float(ys - ysb), float(zs - zsb), float(ws - wsb)

        # Unskewed offsets
        ssi = (xsi + ysi + zsi + wsi) * -0.138196601125011
        xi, yi, zi, wi = xsi + ssi, ysi + ssi, zsi + ssi, wsi + ssi

        index = \
            (((xsb * 4) & 3) << 0) \
            | (((ysb * 4) & 3) << 2) \
            | (((zsb * 4) & 3) << 4) \
            | (((wsb * 4) & 3) << 6)

        # Point contributions
        #  foreach (LatticePoint4D c in LOOKUP_4D[index])
        for c in LOOKUP_4D[index]:
            dx, dy, dz, dw = xi + c.dx, yi + c.dy, zi + c.dz, wi + c.dw
            attn = 0.8 - dx * dx - dy * dy - dz * dz - dw * dw
            if attn < 0:
                continue

            attn *= attn
            pxm, pym = int(xsb + c.xsv) & PMASK, int(ysb + c.ysv) & PMASK
            pzm, pwm = int(zsb + c.zsv) & PMASK, int(wsb + c.wsv) & PMASK
            grad = self._permGrad4[self._perm[self._perm[self._perm[pxm] ^ pym] ^ pzm] ^ pwm]
            extrapolation = grad.dx * dx + grad.dy * dy + grad.dz * dz + grad.dw * dw
            value += attn * attn * extrapolation

        return value
