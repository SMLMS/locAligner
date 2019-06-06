# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 15:19:22 2019

@author: malkusch

run with
python setup.py sdist bdist_wheel
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="locAligner",
    version="19.04",
    author="Sebastian Malkusch",
    author_email="malkusch@chemie.uni-frankfurt.com",
    description="a package for registering single molecule localization microscopy datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SMLMS/locAligner",
    packages=setuptools.find_packages(),
	install_requires=['numpy',
						'matplotlib',
                        'pandas',
						'scipy',
                        'sklearn',
						'IPython',
						'ipywidgets',
						'hide_code'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0 License",
        "Operating System :: OS Independent",
    ],
)