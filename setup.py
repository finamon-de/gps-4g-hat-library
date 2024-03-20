# call: python.exe setup.py sdist bdist_wheel
# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="gps4ghat",
    version="0.2.0",
    description="python library for Finamon GNSS/4G Modem HAT Shield",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://finamon.de/",
    author="Finamon",
    author_email="info@finamon.de",
    license="TBD",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: TBD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=["gps4ghat"],
    include_package_data=True,
    install_requires=[
        "pynmea2",
        "python-dotenv"
        ]
)

