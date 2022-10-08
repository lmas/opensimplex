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
line_stack = opensimplex.double_polar_loop_1D_stack(
    N_frames=N_FRAMES,
    N_pixels_x=N_PIXELS,
    t_step=0.1,
    x_step=1 / FEATURE_SIZE,
    seed=3,
    verbose=True,
    dtype=np.float32,
)

# Plot
fig, ax = plt.subplots()
(line,) = ax.plot(line_stack[0])
ax.set_xlim((0, len(line_stack[0])))
ax.set_ylim((-1, 1))
frame_text = ax.text(0, 1.02, "", transform=ax.transAxes)


def anim_init():
    line.set_ydata(line_stack[0])
    frame_text.set_text("")
    return line, frame_text


def anim_fun(j):
    line.set_ydata(line_stack[j])
    frame_text.set_text(f"frame {j:03d}")
    return line, frame_text


anim = animation.FuncAnimation(
    fig,
    anim_fun,
    frames=len(line_stack),
    interval=40,
    init_func=anim_init,
    # blit=True,
)

# plt.grid(False)
# plt.axis("off")
plt.show()

# anim.save("polar_loop_1D_stack.gif", dpi=69, writer="imagemagick", fps=25)
