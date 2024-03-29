# -*- coding: utf-8 -*-
"""setup script"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyqttable",
    version="0.0.2",
    author="Tongyan Xu",
    author_email="tyxu18@gmail.com",
    description="A simple configurable table widget based on PyQt5 and pandas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TongyanXu/pyqttable",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # install_requires=[
    #     'PyQt5',
    #     'pandas',
    # ],
)
