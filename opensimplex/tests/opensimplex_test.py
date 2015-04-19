
from PIL import Image # Depends on the Pillow lib

from opensimplex import OpenSimplex

WIDTH = 512
HEIGHT = 512
FEATURE_SIZE = 24.0


def main():
    simplex = OpenSimplex()

    print('Generating 2D image...')
    im = Image.new('L', (WIDTH, HEIGHT))
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            value = simplex.noise2d(x / FEATURE_SIZE, y / FEATURE_SIZE)
            color = int((value + 1) * 128)
            im.putpixel((x, y), color)
    im.save('noise2d.png')

    print('Generating 2D slice of 3D...')
    im = Image.new('L', (WIDTH, HEIGHT))
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            value = simplex.noise3d(x / FEATURE_SIZE, y / FEATURE_SIZE, 0.0)
            color = int((value + 1) * 128)
            im.putpixel((x, y), color)
    im.save('noise3d.png')

    print('Generating 2D slice of 4D...')
    im = Image.new('L', (WIDTH, HEIGHT))
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            value = simplex.noise4d(x / FEATURE_SIZE, y / FEATURE_SIZE, 0.0, 0.0)
            color = int((value + 1) * 128)
            im.putpixel((x, y), color)
    im.save('noise4d.png')


if __name__ == '__main__':
    main()
