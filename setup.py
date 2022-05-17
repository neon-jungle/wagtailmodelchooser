#!/usr/bin/env python
"""
Install wagtailmodelchooser using setuptools
"""
from setuptools import find_packages, setup

with open('wagtailmodelchooser/version.py', 'r') as f:
    version = None
    exec(f.read())

with open('README.rst', 'r') as f:
    readme = f.read()

setup(
    name='wagtail-modelchooser',
    version=version,
    description='Model choosers for Wagtail admin',
    long_description=readme,
    author='Tim Heap',
    author_email='developers@neonjungle.studio',
    url='https://github.com/takeflight/wagtailmodelchooser/',

    install_requires=['wagtail>=2.2'],
    zip_safe=False,
    license='BSD License',

    packages=find_packages(exclude=['tests*']),

    include_package_data=True,
    package_data={},

    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
    ],
)
