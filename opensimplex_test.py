import random
import time
from PIL import Image # Depends on the Pillow lib

from opensimplex import OpenSimplexNoise

WIDTH = 512
HEIGHT = 512
FEATURE_SIZE = 24

def main():
    random.seed(time.time())
    seed = random.randint(0, 100000)
    simplex = OpenSimplexNoise(seed)
    im = Image.new('L', (WIDTH, HEIGHT))

    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            value = simplex.noise2d(x / FEATURE_SIZE, y / FEATURE_SIZE)
            color = int((value + 1) * 128)
            im.putpixel((x, y), color)

    im.show()

if __name__ == '__main__':
    main()
