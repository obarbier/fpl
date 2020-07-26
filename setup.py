#!/usr/bin/env python

"""The setup script."""
import os

from setuptools import setup, find_packages


# Get a list of all files in the JS directory to include in our module
def package_files(directory):
    paths = []
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


js_files = package_files('fplsupercharge/server/js/build')
with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []
# FIXME: change the inport statement
# with open('requirements_dev.txt') as lines:
#     requirements = [line.rstrip() for line in lines]


setup_requirements = ["click>=7.0",
                      "flask",
                      "uplink>=0.9.1",
                      "gunicorn==20.0.4",
                        'waitress; platform_system == "Windows"',
                        'gunicorn; platform_system != "Windows"',
                      "protobuf==3.12.2",
                      "fpl"
                      ]
# FIXME: change author email
test_requirements = [ "tox==3.14.0", "flake8==3.7.8"]

setup(
    author="Olivier Cedric Barbier",
    author_email='obarbier13@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="an fpl wrapper that will allow you to compete in the best league",
    entry_points={
        'console_scripts': [
            'fplsupercharge=fplsupercharge.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='fplsupercharge',
    name='fplsupercharge',
    packages=find_packages(include=['fplsupercharge', 'fplsupercharge.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/obarbier/fplsupercharge',
    version='0.1.0',
    zip_safe=False,
)
