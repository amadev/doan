#!/usr/bin/env python

from setuptools import setup, find_packages
setup(
    name = "doan",
    version = "0.1.0.dev0",
    packages = find_packages(),
    # metadata for upload to PyPI
    author = "Andrey Volkov",
    author_email = "amadev@mail.ru",
    description = "Simple library for analytics",
    license = "MIT",
    keywords = "analytics statistics",
    url = "https://github.com/amadev/doan",
)
