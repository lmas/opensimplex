#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Dennis van Gils (https://github.com/Dennis-van-Gils)

import sys

try:
    from matplotlib import pyplot as plt
except ImportError:
    sys.exit("This demo requires the `matplotlib` package.")

import numpy as np
import opensimplex

N_PIXELS = 256
FEATURE_SIZE = 24.0

# Generate noise
noise = opensimplex.tileable_2D_image(
    N_pixels_x=N_PIXELS,
    N_pixels_y=N_PIXELS,
    x_step=1 / FEATURE_SIZE,
    y_step=1 / FEATURE_SIZE,
    seed=3,
    verbose=True,
)

# Plot
fig, ax = plt.subplots()
img = ax.imshow(
    np.tile(noise, (3, 3)),
    cmap="gray",
    vmin=-1,
    vmax=1,
    interpolation="none",
)

h, w = np.shape(noise)
plt.plot((0, 0, w, w), (0, h, h, 0), "r-")
plt.grid(False)
plt.axis("off")
plt.show()

# fig.savefig(
#     "demo_tileable_2D_image.png", dpi=69 * 3, bbox_inches="tight", pad_inches=0
# )
