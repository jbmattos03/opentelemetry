from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("app_collector_local.py")
)