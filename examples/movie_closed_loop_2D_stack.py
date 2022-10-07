#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Dennis van Gils (https://github.com/Dennis-van-Gils)

from matplotlib import pyplot as plt
from matplotlib import animation

import opensimplex

N_PIXELS = 100  # Number of pixels on a single axis
N_FRAMES = 20  # Number of time frames

# Generate noise
img_stack = opensimplex.closed_loop_2D_stack(
    N_pixels=N_PIXELS,
    N_frames=N_FRAMES,
    t_step=0.1,
    x_step=0.05,
    seed=3,
    verbose=True,
)

# Plot
fig_1 = plt.figure()
ax = plt.axes()
img = plt.imshow(
    img_stack[0],
    cmap="gray",
    vmin=-1,
    vmax=1,
    interpolation="none",
)
frame_text = ax.text(0, 1.02, "", transform=ax.transAxes)


def init_anim():
    img.set_data(img_stack[0])
    frame_text.set_text("")
    return img, frame_text


def anim(j):
    img.set_data(img_stack[j])
    frame_text.set_text(f"frame {j:03d}")
    return img, frame_text


ani = animation.FuncAnimation(
    fig_1,
    anim,
    frames=N_FRAMES,
    interval=40,
    init_func=init_anim,
    # blit=True,
)

# plt.grid(False)
# plt.axis("off")
plt.show()
