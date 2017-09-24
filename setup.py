#!/usr/bin/env python

from setuptools import setup, find_packages
setup(
    name="doan",
    version="0.2.3",
    packages=find_packages(),
    # metadata for upload to PyPI
    author="Andrey Volkov",
    author_email="amadev@mail.ru",
    description="Simple library for analytics",
    license="MIT",
    keywords="analytics statistics",
    url="https://github.com/amadev/doan",
    install_requires=[
        'matplotlib>=1.5.1',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
)
