from distutils.core import setup, Extension
from Cython.Distutils import build_ext
import numpy

## \file setup.py setup.py
#  \brief The python script for building proteus
#
#  Set the DISTUTILS_DEBUG environment variable to print detailed information while setup.py is running.
#
try:
    import sys,os.path
    sys.path.insert(0,os.path.join(sys.prefix,'proteusConfig'))
    from config import *
except:
    raise RuntimeError("Missing or invalid config.py file. See proteusConfig for examples")

###to turn on debugging in c++
##\todo Finishing cleaning up setup.py/setup.cfg, config.py...
from distutils import sysconfig
cv = sysconfig.get_config_vars()
cv["OPT"] = cv["OPT"].replace("-g","")
cv["CFLAGS"] = cv["CFLAGS"].replace("-g","")


setup(name='proteus_mprans',
      version='0.9.0',
      description='Proteus modules for simulating free surface fluid/structure interaction',
      author='Chris Kees',
      author_email='christopher.e.kees@usace.army.mil',
      url='https://adh.usace.army.mil/proteus',
      packages=['proteus.mprans'],
      package_dir={'proteus.mprans':'mprans'},
      ext_package='proteus.mprans',
      cmdclass = {'build_ext':build_ext},
      ext_modules=[Extension('cRANS2PV2',
                             ['mprans/cRANS2PV2Module.cpp','mprans/RANS2PV2.cpp'],
                             define_macros=[('PROTEUS_SUPERLU_H',PROTEUS_SUPERLU_H),('VRANS',1)],
                             include_dirs=[numpy.get_include(),PROTEUS_INCLUDE_DIR,os.getenv('PROTEUS')+'/proteusModule/include',os.getenv('PROTEUS')+'/proteusModule/src',
                                           PROTEUS_SUPERLU_INCLUDE_DIR],
                             libraries=['m'],
                             extra_compile_args=PROTEUS_EXTRA_COMPILE_ARGS,
                             extra_link_args=PROTEUS_EXTRA_LINK_ARGS),
                   Extension('cNCLSV2',
                             ['mprans/cNCLSV2Module.cpp','mprans/NCLSV2.cpp'],
                             define_macros=[('PROTEUS_SUPERLU_H',PROTEUS_SUPERLU_H)],
                             include_dirs=[numpy.get_include(),PROTEUS_INCLUDE_DIR,os.getenv('PROTEUS')+'/proteusModule/include',os.getenv('PROTEUS')+'/proteusModule/src',
                                           PROTEUS_SUPERLU_INCLUDE_DIR],
                             libraries=['m'],
                             extra_compile_args=PROTEUS_EXTRA_COMPILE_ARGS,
                             extra_link_args=PROTEUS_EXTRA_LINK_ARGS),
                   Extension('cVOFV2',
                             ['mprans/cVOFV2Module.cpp','mprans/VOFV2.cpp'],
                             define_macros=[('PROTEUS_SUPERLU_H',PROTEUS_SUPERLU_H),('VRANS',1)],
                             include_dirs=[numpy.get_include(),PROTEUS_INCLUDE_DIR,os.getenv('PROTEUS')+'/proteusModule/include',os.getenv('PROTEUS')+'/proteusModule/src',
                                           PROTEUS_SUPERLU_INCLUDE_DIR],
                             libraries=['m'],
                             extra_compile_args=PROTEUS_EXTRA_COMPILE_ARGS,
                             extra_link_args=PROTEUS_EXTRA_LINK_ARGS),
                   Extension('cRDLSV2',
                             ['mprans/cRDLSV2Module.cpp','mprans/RDLSV2.cpp'],
                             define_macros=[('PROTEUS_SUPERLU_H',PROTEUS_SUPERLU_H)],
                             include_dirs=[numpy.get_include(),PROTEUS_INCLUDE_DIR,os.getenv('PROTEUS')+'/proteusModule/include',os.getenv('PROTEUS')+'/proteusModule/src',
                                           PROTEUS_SUPERLU_INCLUDE_DIR],
                             libraries=['m'],
                             extra_compile_args=PROTEUS_EXTRA_COMPILE_ARGS,
                             extra_link_args=PROTEUS_EXTRA_LINK_ARGS),
                   Extension('cMCorrV2',
                             ['mprans/cMCorrV2Module.cpp','mprans/MCorrV2.cpp'],
                             define_macros=[('PROTEUS_SUPERLU_H',PROTEUS_SUPERLU_H)],
                             include_dirs=[numpy.get_include(),PROTEUS_INCLUDE_DIR,os.getenv('PROTEUS')+'/proteusModule/include',os.getenv('PROTEUS')+'/proteusModule/src',
                                           PROTEUS_SUPERLU_INCLUDE_DIR],
                             libraries=['m'],
                             extra_compile_args=PROTEUS_EXTRA_COMPILE_ARGS,
                             extra_link_args=PROTEUS_EXTRA_LINK_ARGS),
                   Extension("cNCLS",["mprans/cNCLS.pyx"],depends=["mprans/NCLS.h"], language="c++",include_dirs=[numpy.get_include(),os.getenv('PROTEUS')+'/proteusModule/include',os.getenv('PROTEUS')+'/proteusModule/src']),
                   Extension("cMCorr",["mprans/cMCorr.pyx"],depends=["mprans/MCorr.h"], define_macros=[('PROTEUS_LAPACK_H',PROTEUS_LAPACK_H),
                                            ('PROTEUS_LAPACK_INTEGER',PROTEUS_LAPACK_INTEGER),
                                            ('PROTEUS_BLAS_H',PROTEUS_BLAS_H)],language="c++",include_dirs=[numpy.get_include(),os.getenv('PROTEUS')+'/proteusModule/include',os.getenv('PROTEUS')+'/proteusModule/src'],
                             library_dirs=[PROTEUS_LAPACK_LIB_DIR,
                                           PROTEUS_BLAS_LIB_DIR],
                             libraries=['m',PROTEUS_LAPACK_LIB,PROTEUS_BLAS_LIB],
                             extra_compile_args=PROTEUS_EXTRA_COMPILE_ARGS,
                             extra_link_args=PROTEUS_EXTRA_LINK_ARGS),
                   Extension("cRANS2P",["mprans/cRANS2P.pyx"],
		             depends=["mprans/RANS2P.h",os.getenv('PROTEUS')+'/proteusModule/include/ModelFactory.h',os.getenv('PROTEUS')+'/proteusModule/src/CompKernel.h'],
			     language="c++",
			     include_dirs=[numpy.get_include(),os.getenv('PROTEUS')+'/proteusModule/include',os.getenv('PROTEUS')+'/proteusModule/src']),
                   Extension("cRANS2P2",["mprans/cRANS2P2.pyx"],
		             depends=["mprans/RANS2P2.h",os.getenv('PROTEUS')+'/proteusModule/include/ModelFactory.h',os.getenv('PROTEUS')+'/proteusModule/src/CompKernel.h'], 
		             language="c++",
			     include_dirs=[numpy.get_include(),os.getenv('PROTEUS')+'/proteusModule/include',os.getenv('PROTEUS')+'/proteusModule/src']),                 
		   Extension("cRBLES",["mprans/cRBLES.pyx"],
		             depends=["mprans/RBLES.h",os.getenv('PROTEUS')+'/proteusModule/include/ModelFactory.h',os.getenv('PROTEUS')+'/proteusModule/src/CompKernel.h'],
		             language="c++",
			     include_dirs=[numpy.get_include(),os.getenv('PROTEUS')+'/proteusModule/include',os.getenv('PROTEUS')+'/proteusModule/src']),
                   Extension("cVRANS2P",["mprans/cVRANS2P.pyx"],
		             depends=["mprans/VRANS2P.h",os.getenv('PROTEUS')+'/proteusModule/include/ModelFactory.h',os.getenv('PROTEUS')+'/proteusModule/src/CompKernel.h'], 
		             language="c++",
			     include_dirs=[numpy.get_include(),os.getenv('PROTEUS')+'/proteusModule/include',os.getenv('PROTEUS')+'/proteusModule/src']),
                   Extension("cRDLS",["mprans/cRDLS.pyx"],
		             depends=["mprans/RDLS.h",os.getenv('PROTEUS')+'/proteusModule/include/ModelFactory.h',os.getenv('PROTEUS')+'/proteusModule/src/CompKernel.h'], 
		             language="c++",
			     include_dirs=[numpy.get_include(),os.getenv('PROTEUS')+'/proteusModule/include',os.getenv('PROTEUS')+'/proteusModule/src']),
                   Extension("cVOF",["mprans/cVOF.pyx"],
		             depends=["mprans/VOF.h",os.getenv('PROTEUS')+'/proteusModule/include/ModelFactory.h',os.getenv('PROTEUS')+'/proteusModule/src/CompKernel.h'], 
		             language="c++",
			     include_dirs=[numpy.get_include(),os.getenv('PROTEUS')+'/proteusModule/include',os.getenv('PROTEUS')+'/proteusModule/src']),
                   Extension("cVolumeAveragedVOF",["mprans/cVolumeAveragedVOF.pyx"],
		             depends=["mprans/VolumeAveragedVOF.h",os.getenv('PROTEUS')+'/proteusModule/include/ModelFactory.h',os.getenv('PROTEUS')+'/proteusModule/src/CompKernel.h'], 
		             language="c++",
			     include_dirs=[numpy.get_include(),os.getenv('PROTEUS')+'/proteusModule/include',os.getenv('PROTEUS')+'/proteusModule/src']),
                   Extension("cMoveMesh",["mprans/cMoveMesh.pyx"],
		             depends=["mprans/MoveMesh.h",os.getenv('PROTEUS')+'/proteusModule/include/ModelFactory.h',os.getenv('PROTEUS')+'/proteusModule/src/CompKernel.h'], 
		             language="c++",
			     include_dirs=[numpy.get_include(),os.getenv('PROTEUS')+'/proteusModule/include',os.getenv('PROTEUS')+'/proteusModule/src']),
                   Extension("cSW2D",["mprans/cSW2D.pyx"],
		             depends=["mprans/SW2D.h",os.getenv('PROTEUS')+'/proteusModule/include/ModelFactory.h',os.getenv('PROTEUS')+'/proteusModule/src/CompKernel.h'], 
		             language="c++",
			     include_dirs=[numpy.get_include(),os.getenv('PROTEUS')+'/proteusModule/include',os.getenv('PROTEUS')+'/proteusModule/src'],
                             extra_compile_args=PROTEUS_EXTRA_COMPILE_ARGS+['-g'],
                             extra_link_args=PROTEUS_EXTRA_LINK_ARGS+['-g']),
                   Extension("cSW2DCV",["mprans/cSW2DCV.pyx"],
		             depends=["mprans/SW2DCV.h",os.getenv('PROTEUS')+'/proteusModule/include/ModelFactory.h',os.getenv('PROTEUS')+'/proteusModule/src/CompKernel.h'], 
		             language="c++",
			     include_dirs=[numpy.get_include(),os.getenv('PROTEUS')+'/proteusModule/include',os.getenv('PROTEUS')+'/proteusModule/src'],
                             extra_compile_args=PROTEUS_EXTRA_COMPILE_ARGS+['-g'],
                             extra_link_args=PROTEUS_EXTRA_LINK_ARGS+['-g']),
                   ],
      requires=['numpy']
      )
