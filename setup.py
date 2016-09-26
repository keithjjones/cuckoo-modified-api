from distutils.core import setup
from pip.req import parse_requirements
from setuptools import find_packages

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("requirements.txt")

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='cuckoo-modified-api',
    version='20160926.1',
    author='Keith J. Jones',
    author_email='keith@keithjjones.com',
    packages=find_packages(),
    url='https://github.com/keithjjones/cuckoo-modified-api',
    license='LICENSE',
    description=('A Python library to '
                 'interface with a cuckoo-modified instance'),
    long_description=open('README.MD').read(),
    install_requires=reqs,
    entry_points={
        'console_scripts': [
            'CuckooAPI = CuckooAPI.__main__:main'
        ]
    }
)
