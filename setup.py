import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='cuckoo-modified-api',
    version='20160927.1',
    author='Keith J. Jones',
    author_email='keith@keithjjones.com',
    packages=['CuckooAPI'],
    url='https://github.com/keithjjones/cuckoo-modified-api',
    license='LICENSE',
    description=('A Python library to '
                 'interface with a cuckoo-modified instance'),
    long_description=read('README.TXT'),
    install_requires=['requests[security]'],
)
