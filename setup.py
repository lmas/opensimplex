
from setuptools import setup, find_packages

from opensimplex import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='opensimplex',
    version=__version__,
    description='OpenSimplex n-dimensional gradient noise function.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='opensimplex simplex noise 2D 3D 4D',
    url='https://github.com/lmas/opensimplex',
    download_url='https://github.com/lmas/opensimplex/releases',
    author='A. Svensson',
    author_email='opensimplex@lmas.se',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    python_requires='>=3.6',
)
