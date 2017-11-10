from setuptools import setup
import sys
sys.path.append('builder/')
from conf import source_version

__author__ = 'huang.andrew12@gmail.com'
__copyright__ = 'Andrew Huang'

setup(name='ahh',
      version=source_version,
      packages=['ahh'],
      install_requires=[
                        'matplotlib',
                        'numpy',
                        'pandas',
                        'xarray',
                        'netCDF4',
                        'bokeh',
                        'scipy',
                        ],
      )
