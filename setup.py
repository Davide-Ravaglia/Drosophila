#!/usr/bin/env python

import io
import os
import sys
from shutil import rmtree

try:
  from setuptools import setup, Extension, find_packages
except ImportError:
  from distutils.core import setup, Extension, find_packages

from distutils.sysconfig import customize_compiler

# Package meta-data.
NAME = 'Drosophila'
DESCRIPTION = 'Study on the effect of drugs on Drosophila.'
URL = 'https://github.com/Davide-Ravaglia/Drosophila'
EMAIL = ['davide.ravaglia3@studio.unibo.it', 'nico.curti2@unibo.it']
AUTHOR = ['Davide Ravaglia', 'Nico Curti']
REQUIRES_PYTHON = '>=2.7'
VERSION = None
KEYWORDS = 'drosophila dynamics drugs'

# What packages are required for this module to be executed?
def get_requires():
  with open('requirements.txt', 'r') as f:
    requirements = f.read()
  return list(filter(lambda x: x != '', requirements.split()))

# What packages are optional?
EXTRAS = {
  'tests': [],
}

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
  with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()
except FileNotFoundError:
  long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
  with open(os.path.join(here, 'Drosophila', '__version__.py')) as f:
    exec(f.read(), about)
else:
  about['__version__'] = VERSION


# Where the magic happens:
setup(
  name=NAME,
  version=about['__version__'],
  description=DESCRIPTION,
  long_description=long_description,
  long_description_content_type='text/markdown',
  author=AUTHOR,
  author_email=EMAIL,
  maintainer=AUTHOR,
  maintainer_email=EMAIL,
  python_requires=REQUIRES_PYTHON,
  url=URL,
  download_url=URL,
  keywords=KEYWORDS,
  packages=find_packages(include=['Drosophila'], exclude=('wip', 'test',)),
  # If your package is a single module, use this instead of 'packages':
  #py_modules=['walkers'],
  #
  # entry_points={
  #     'console_scripts': ['mycli=mymodule:cli'],
  # },
  install_requires=get_requires(),
  extras_require=EXTRAS,
  include_package_data=True,
  license='GNU Lesser General Public License v2 or later (LGPLv2+)',
  platforms='any',
  classifiers=[
    # Trove classifiers
    # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    'License :: OSI Approved :: GPL License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy'
  ],
)
