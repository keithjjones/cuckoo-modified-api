from distutils.core import setup

setup(
    name='cuckoo-modified-api',
    version='20160926.1',
    author='Keith J. Jones',
    author_email='keith@keithjjones.com',
    packages=['CuckooAPI'],
    url='https://github.com/keithjjones/cuckoo-modified-api',
    license='LICENSE',
    description=('A Python library to '
                 'interface with a cuckoo-modified instance'),
    long_description=open('README.MD').read(),
    install_requires=["requests[security]"],
    entry_points={
        'console_scripts': [
            'CuckooAPI = CuckooAPI.__main__:main'
        ]
    }
)
