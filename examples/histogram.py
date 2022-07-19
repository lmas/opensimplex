from opensimplex import OpenSimplex
import random, math

buckets = 20
samples = 1000000
rng_range = 100000
char_width = 50

os = OpenSimplex(0)
histogram2 = [0] * (buckets)
histogram3 = [0] * (buckets)
histogram4 = [0] * (buckets)

for i in range(samples):
	x = random.uniform(-rng_range, rng_range)
	y = random.uniform(-rng_range, rng_range)
	z = random.uniform(-rng_range, rng_range)
	w = random.uniform(-rng_range, rng_range)
	v2 = os.noise2(x, y)
	b2 = round((v2+1) / 2 * (buckets-1))
	histogram2[b2] += 1
	v3 = os.noise3(x, y, z)
	b3 = round((v3+1) / 2 * (buckets-1))
	histogram3[b3] += 1
	v4 = os.noise4(x, y, z, w)
	b4 = round((v4+1) / 2 * (buckets-1))
	histogram4[b4] += 1

def print_histogram(histogram):
	biggest = max(histogram)
	for i in range(buckets):
		v = histogram[i]
		n = ((i+0.5) / buckets) * 2 - 1
		w = char_width * v / biggest
		c = ''.join(['*'] * round(w))
		print(f'{n: .2f} {c}')

print("\t2D Noise")
print_histogram(histogram2)
print("\t3D Noise")
print_histogram(histogram3)
print("\t4D Noise")
print_histogram(histogram4)
