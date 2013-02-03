#!/usr/bin/env python
from setuptools import setup


setup(
    name='mygithubprojects',
    version='0.1',
    description='Fetch projects you work on in Github.',
    long_description=open('README.md').read(),
    author='Ratnadeep Debnath',
    author_email='rtnpro@gmail.com',
    modules=[
        'mygithubprojects',
    ],
    install_requires=['PyGithub']
)
