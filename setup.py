#!/usr/bin/env python3

from setuptools import setup

from stonky.__version__ import VERSION

with open("readme.md", "r") as fp:
    LONG_DESCRIPTION = fp.read()

with open("requirements.txt", "r") as fp:
    REQUIREMENTS = fp.read().splitlines()

setup(
    author="Jessy Williams",
    author_email="jessy@jessywilliams.com",
    description="A simple command line dashboard for monitoring stocks",
    entry_points={"console_scripts": ["stonky=stonky.__main__:main"]},
    include_package_data=True,
    install_requires=REQUIREMENTS,
    license="MIT",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    name="stonky",
    packages=["stonky"],
    package_data={"stonky": ["__example.cfg"]},
    python_requires="~=3.6",
    url="https://github.com/jkwill87/stonky",
    version=VERSION,
)
