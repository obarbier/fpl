import os
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="fpl-manage",
    version="0.0.1",
    author="Olivier Barbier",
    author_email="obarbier",
    description="package to help improve my fpl standing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
        install_requires=[
        'protobuf>=3.12.0',
    ]
)    