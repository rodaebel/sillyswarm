# -*- coding: utf-8 -*-
"""Setup script."""

import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name='sillyswarm',
    version='1.0.0',
    author="Tobias Rodäbel",
    author_email="tobias.rodaebel@googlemail.com",
    description="Browser game to demonstrate TyphoonAE's Web Socket Service.",
    long_description=(
        read('README.rst')
        + '\n\n' +
        read('CHANGES.rst')
        ),
    license="Apache License 2.0",
    keywords="google appengine gae web socket html5",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
        ],
    url='',
    packages=find_packages(),
    package_dir = {'': os.sep.join(['src', 'sillyswarm'])},
    include_package_data=True,
    install_requires=[
        'distribute',
    ],
    zip_safe=False,
)
