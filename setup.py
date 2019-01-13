#!/usr/bin/env python

import setuptools

setuptools.setup(
    name='calculator-flask',
    version='1.0',
    packages=['calculator_flask'],
    # description=open(join(dirname(__file__), 'README.txt')).read(),
    entry_points={
        'console_scripts': ['calculator-flask = calculator_flask.server.server:main']
    },
    install_requires=[
        'Flask>=1.0.0'
    ],
)
