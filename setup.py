from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='trigger',
    version='0.1.0dev0',
    author='Felix Wagner',
    author_email="felix.wagner@oeaw.ac.at",
    description='Numba-accelerated peak detection for continuously sampled sensor signals..',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fewagner/trigger",
    license='GPLv3',
    packages=find_packages(include=['trigger', 'trigger.*']),
    install_requires=['h5py>=3.2',
                      'pickle-mixin>=1.0',
                      'numpy>=1.19',
                      'matplotlib>=3.3',
                      'scipy>=1.6',
                      'numba>=0.54',
                      'tqdm>=4.62',
                      'pyfftw',
                      ],
    python_requires='>=3.8',
)
