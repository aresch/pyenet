from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import glob
import sys
import os

compile_options = {
  'hide_socket_fileno': False,
  'fast_connect_drop': False,
}

if "--enable-hide-socket-fileno" in sys.argv:
    compile_options["hide_socket_fileno"] = True
    sys.argv.remove("--enable-hide-socket-fileno")
if "--enable-fast-connect-drop" in sys.argv:
    compile_options["fast_connect_drop"] = True
    sys.argv.remove("--enable-fast-connect-drop")

with open(os.path.join(os.path.dirname(__file__), 'config.pxi'), 'w') as fd:
    for k, v in compile_options.items():
        fd.write('DEF %s = %d\n' % (k.upper(), int(v)))


source_files = ["enet.pyx", "config.pxi"]

_enet_files = glob.glob("enet/*.c")

if not _enet_files:
    print("You need to download and extract the enet 1.3 source to enet/")
    print("Download the source from: http://enet.bespin.org/SourceDistro.html")
    print("See the README for more instructions")
    sys.exit(1)

source_files.extend(_enet_files)

define_macros = [('HAS_POLL', None),
                 ('HAS_FCNTL', None),
                 ('HAS_MSGHDR_FLAGS', None),
                 ('HAS_SOCKLEN_T', None) ]

libraries = []

if sys.platform == 'win32':
    define_macros.extend([('WIN32', None)])
    libraries.extend(['ws2_32', 'Winmm'])

if sys.platform != 'darwin':
    define_macros.extend([('HAS_GETHOSTBYNAME_R', None), ('HAS_GETHOSTBYADDR_R', None)])

ext_modules = [
    Extension(
        "enet",
        extra_compile_args=["-O3"],
        sources=source_files,
        include_dirs=["enet/include/"],
        define_macros=define_macros,
        libraries=libraries)]

setup(
  name = 'enet',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)
