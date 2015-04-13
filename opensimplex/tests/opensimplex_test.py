
from PIL import Image # Depends on the Pillow lib

from opensimplex import OpenSimplexNoise

WIDTH = 512
HEIGHT = 512
FEATURE_SIZE = 24.0

def generate_image(filename, noise_func):
    im = Image.new('L', (WIDTH, HEIGHT))

    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            value = noise_func(x / FEATURE_SIZE, y / FEATURE_SIZE)
            color = int((value + 1) * 128)
            im.putpixel((x, y), color)

    im.save(filename)
    return im


def main():
    simplex = OpenSimplexNoise()

    print 'Generating 2D image...'
    noise2d = generate_image('noise2d.png', simplex.noise2d)
    print 'Generating 2D image of 3D slice...'
    noise3d = generate_image('noise3d.png', simplex.noise3d)


if __name__ == '__main__':
    main()
