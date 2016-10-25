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
    name='wagtailmodelchooser',
    version=version,
    description='Model choosers for Wagtail admin',
    long_description=readme,
    author='Tim Heap',
    author_email='tim@takeflight.com.au',
    url='https://github.com/takeflight/wagtailmodelchooser/',

    install_requires=['wagtail>=1.7'],
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
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
    ],
)
