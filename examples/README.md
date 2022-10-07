
# Examples

- [distribution.m](./distribution.m): Matlab script to generate nice histogram for noise distributions.
- [histogram.py](./histogram.py): Python script to to generate same histogram, but in a CLI environment.
- [images.py](./images.py): Visualise noise on 2D images.
- [movie_closed_loop_2D_stack.py](./movie_closed_loop_2D_stack.py): Generates a matplotlib movie showcasing the `closed_loop_2D_stack()` function. It generates Simplex noise as 2D bitmap images that animate over time in a closed-loop fashion. I.e., the bitmap image of the last time frame will smoothly animate into the bitmap image of the first time frame again. The animation path is /not/ a simple reversal of time in order to have the loop closed, but rather is a fully unique path from start to finish.