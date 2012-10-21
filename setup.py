#! /usr/bin/env python

# Public Domain (-) 2004-2012 The Assetgen Authors.
# See the Assetgen UNLICENSE file for details.

from assetgen.version import __release__
from setuptools import setup

# ------------------------------------------------------------------------------
# Run Setup
# ------------------------------------------------------------------------------

setup(
    name="assetgen",
    author="tav",
    author_email="tav@espians.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: Public Domain",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Text Processing",
        "Topic :: Utilities"
        ],
    description="Asset generator for modern web app development",
    entry_points=dict(console_scripts=[
        "assetgen = assetgen.main:main"
        ]),
    install_requires=[
        "PyYAML >= 3.09",
        "requests >= 0.14.1",
        "simplejson >= 2.1.6",
        "tavutil >= 1.0"
        ],
    keywords=[
        "assets", "javascript", "css", "coffeescript", "sass", "typescript",
        "less", "lessjs", "scss", "stylus", "source maps", "i18n"
        ],
    license="Public Domain",
    long_description=open('README.rst').read(),
    packages=["assetgen"],
    url="https://github.com/tav/assetgen",
    version=__release__,
    zip_safe=True
    )
