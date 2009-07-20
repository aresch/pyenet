#!/usr/bin/env python

# see http://www.python.org/doc/current/dist/setup-script.html
#  for distutil options.
#
# Original version by Rene Dudfield <illumen@yahoo.com>
# Modifications by Andrew Resch <andrewresch@gmail.com>
#

import sys, os, os.path
from distutils.core import setup, Extension

source_dirs = ['enet']
define_macros = [('HAS_GETHOSTBYNAME_R', None),
                 ('HAS_GETHOSTBYADDR_R', None),
                 ('HAS_POLL', None),
                 ('HAS_FCNTL', None),
                 ('HAS_MSGHDR_FLAGS', None),
                 ('HAS_SOCKLEN_T', None) ]

libraries = []

# For enet.pyx

os.system("pyrexc enet.pyx")
source_files = ['enet.c']

# Build a list of all the source files
for dir in source_dirs:
    for file in os.listdir(dir):
        if '.c' == os.path.splitext(file)[1]:
            source_files.append(dir + '/' + file)

# Additional Windows dependencies
if sys.platform == 'win32':
    define_macros.append(('WIN32', None))
    libraries.append('ws2_32')

# Go force and multiply
setup(name="enet", version="1.2",
      ext_modules=[Extension("enet",
                             source_files,
                             include_dirs=["enet/include/"],
			     define_macros=define_macros,
			     libraries=libraries,
			     library_dirs=[]
			    )
		  ]
    )
