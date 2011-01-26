from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("fvector", ["fast_vector.pyx"])]

setup(
  name = 'vector',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)

#python setup.py build_ext --inplace
