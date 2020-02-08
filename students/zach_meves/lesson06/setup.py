"""
Compile Cython code, ``good_perf_cython.pyx``
"""

from distutils.core import setup
from Cython.Build import cythonize

setup(name="GoodPerf",
      ext_modules=cythonize("good_perf_cython.pyx"))
