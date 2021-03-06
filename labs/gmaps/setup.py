from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [ 
                Extension("traverser", ["traverser.pyx"]),
                Extension("fast_dart", ["fast_darts.pyx"])
                ]

setup(
  name = 'traverser',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)

#python setup.py build_ext --inplace
