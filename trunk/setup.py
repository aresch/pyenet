#
# setup.py
#
# Copyright (C) 2010 Andrew Resch <andrewresch@gmail.com>
#
# pyenet is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# pyenet is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
#     The Free Software Foundation, Inc.,
#     51 Franklin Street, Fifth Floor
#     Boston, MA  02110-1301, USA.
#

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import glob
import sys

source_files = ["enet.pyx"]

_enet_files = glob.glob("enet/*.c")

if not _enet_files:
    print "You need to download and extract the enet 1.3 source to enet/"
    print "Download the source from: http://enet.bespin.org/SourceDistro.html"
    print "See the README for more instructions"
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
