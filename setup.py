
from setuptools import setup, find_packages

from opensimplex import __version__, __author__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='opensimplex',
    version=__version__,
    author=__author__,
    author_email='opensimplex@larus.se',
    description='OpenSimplex n-dimensional gradient noise function.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='opensimplex simplex noise 2D 3D 4D',
    url='https://github.com/lmas/opensimplex',
    download_url='https://github.com/lmas/opensimplex/releases',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
		'numpy>=1.22',
    ],
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    python_requires='>=3.8',
)
