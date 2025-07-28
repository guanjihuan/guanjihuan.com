from setuptools import setup, Extension
import pybind11

setup(
    name='example',
    ext_modules=[
        Extension(
            'example',
            ['example.cpp'],
            include_dirs=[pybind11.get_include()],
            language='c++',
        ),
    ],
)