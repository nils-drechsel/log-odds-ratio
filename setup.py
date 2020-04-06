#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 17:21:39 2020

@author: nils
"""


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LogOddsRatio",
    version="0.0.1",
    author="Nils J. D. Drechsel",
    author_email="nils.drechsel@gmail.com",
    description="Log odd ratio calculation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nils-drechsel/log-odds-ratio",
    packages=["LogOddsRatio"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.8',
    install_requires = ""
)