import json

from os.path import join, dirname
from setuptools import setup, find_packages


# reading package version (same way the sqlalchemy does)
with open(join(dirname(__file__), 'package.json')) as v_file:
    package_version = json.load(v_file)['version']


dependencies = [
    'yhttp >= 3.0.3',
    'yhttp-pony >= 2.2.1',
]


setup(
    name='postmin',
    version=package_version,
    py_modules=['postmin'],
    install_requires=dependencies,
    license='MIT',
    entry_points={
        'console_scripts': [
            'postmin = postmin:app.climain'
        ]
    },

    description='Language for ASCII diagrams.',
)
