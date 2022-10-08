#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Dennis van Gils (https://github.com/Dennis-van-Gils)

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

import opensimplex

N_PIXELS = 256  # Number of pixels on a single axis
N_FRAMES = 50  # Number of time frames
FEATURE_SIZE = 24.0

# Generate noise
img_stack = opensimplex.polar_loop_2D_stack(
    N_frames=N_FRAMES,
    N_pixels_x=N_PIXELS,
    N_pixels_y=N_PIXELS,
    t_step=0.1,
    x_step=1 / FEATURE_SIZE,
    seed=3,
    verbose=True,
    dtype=np.float32,
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

# anim.save("polar_loop_2D_stack.gif", dpi=69, writer="imagemagick", fps=25)
