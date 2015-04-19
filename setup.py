

from setuptools import setup, find_packages

from opensimplex import __version__

setup(
    name='opensimplex',
    version=__version__,
    description='OpenSimplex n-dimensional gradient noise function.',
    long_description=open('README.rst').read(),
    keywords='opensimplex simplex noise 2D 3D 4D',
    url='https://github.com/lmas/opensimplex',
    download_url='https://github.com/lmas/opensimplex/releases',
    author='A. Svensson',
    author_email='lmasvensson@gmail.com',
    license='Public Domain',
    packages=find_packages(),
    install_requires=[],
    scripts=['bin/yanktv'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[ # See: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'License :: Public Domain',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
)

