#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Dennis van Gils (https://github.com/Dennis-van-Gils)

import sys

try:
    from matplotlib import pyplot as plt
    from matplotlib import animation
except ImportError:
    sys.exit("This demo requires the `matplotlib` package.")

import numpy as np
import opensimplex

N_FRAMES = 50
N_PIXELS = 256
FEATURE_SIZE = 24.0

# Generate noise
img_stack = opensimplex.looping_animated_2D_image(
    N_frames=N_FRAMES,
    N_pixels_x=N_PIXELS,
    N_pixels_y=N_PIXELS,
    t_step=0.1,
    x_step=1 / FEATURE_SIZE,
    dtype=np.float32,
    seed=3,
    verbose=True,
)

# Plot
fig, ax = plt.subplots()
img = ax.imshow(
    img_stack[0],
    cmap="gray",
    vmin=-1,
    vmax=1,
    interpolation="none",
)
frame_text = ax.text(0, 1.02, "", transform=ax.transAxes)


def anim_init():
    img.set_data(img_stack[0])
    frame_text.set_text("")
    return img, frame_text


def anim_fun(j):
    img.set_data(img_stack[j])
    frame_text.set_text(f"frame {j:03d}")
    return img, frame_text


anim = animation.FuncAnimation(
    fig,
    anim_fun,
    frames=len(img_stack),
    interval=40,
    init_func=anim_init,
    # blit=True,
)


plt.grid(False)
plt.axis("off")
plt.show()

# anim.save(
#     "demo_looping_animated_2D_image.gif", dpi=69, writer="imagemagick", fps=25
# )
