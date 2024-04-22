#!/usr/bin/python

from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext

module1 = Pybind11Extension(
    'robot_interface',
    sources=['python_interface.cpp'],
)

setup(
    name='robot_interface',
    version='1.0',
    ext_modules=[module1],
    cmdclass={'build_ext': build_ext},
)
