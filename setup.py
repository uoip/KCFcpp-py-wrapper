import sys
from distutils.core import setup, Extension
from Cython.Distutils import build_ext
import numpy
import pkgconfig

if pkgconfig.exists('opencv4'):
	opencv_pkginfo = pkgconfig.parse('opencv4')
	extra_compile_args = ['-std=c++11', '-DUSE_OPENCV4']
elif pkgconfig.exists('opencv'):
	opencv_pkginfo = pkgconfig.parse('opencv')
	extra_compile_args = ['-std=c++11']
else:
	print("opencv package config is not found.", file=sys.stderr)
	exit(1)

libdr = ['/usr/local/lib'] + opencv_pkginfo["library_dirs"]
incdr = [numpy.get_include(), '/usr/local/include/'] + opencv_pkginfo["include_dirs"]

ext = [
	Extension('cvt', ['python/cvt.pyx'], 
		language = 'c++', 
		extra_compile_args = extra_compile_args,
		include_dirs = incdr, 
		library_dirs = libdr, 
		libraries = ['opencv_core']), 
	Extension('KCF', ['python/KCF.pyx', 'src/kcftracker.cpp', 'src/fhog.cpp'], 
		language = 'c++', 
		extra_compile_args = extra_compile_args,
		include_dirs = incdr, 
		library_dirs = libdr, 
		libraries = ['opencv_core', 'opencv_imgproc'])
]

setup(
	name = 'app', 
	cmdclass = {'build_ext':build_ext}, 
	ext_modules = ext
)

#python setup.py build_ext --inplace
