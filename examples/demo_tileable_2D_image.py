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
    seed=5,
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

# Export image to disk
if 0:
    tiled_noise = np.tile((noise + 1) / 2, (3, 3))  # Scaled [0, 1]
    rgb_img = np.ndarray((3 * h, 3 * w, 3))
    rgb_img[:, :, 0] = tiled_noise
    rgb_img[:, :, 1] = tiled_noise
    rgb_img[:, :, 2] = tiled_noise
    rgb_img[0 : h + 1, 0, :] = (1, 0, 0)
    rgb_img[0 : h + 1, w, :] = (1, 0, 0)
    rgb_img[0, 0 : w + 1, :] = (1, 0, 0)
    rgb_img[h, 0 : w + 1, :] = (1, 0, 0)

    plt.imsave("demo_tileable_2D_image.png", rgb_img)
