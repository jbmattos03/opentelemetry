from setuptools import setup
from Cython.Build import cythonize

setup(
    name="local_collector",
    ext_modules=cythonize(["local_collector.pyx"]),
    compiler_directives={"language_level": "3"},
)