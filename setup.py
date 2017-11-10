from setuptools import setup, find_packages
import sys
import glob
sys.path.append('builder/')
from conf import source_version

__author__ = 'huang.andrew12@gmail.com'
__copyright__ = 'Andrew Huang'

setup(name='ahh',
      license='MIT',
      version=source_version,
      description='Functions that I can easily reference, and maybe you too!',
      packages=find_packages(exclude=['cartopy', 'basemap']),
      install_requires=[
                        'matplotlib',
                        'numpy',
                        'pandas',
                        'xarray',
                        'netCDF4',
                        'bokeh',
                        'scipy',
                        ],
      author='Andrew Huang',
      author_email='huang.andrew12@gmail.com',
      url='https://github.com/ahuang11/ahh',
      keywords=['data', 'visualization',
                'analysis', 'streamline',
                'andrew', 'huang', 'helps'],
      include_package_data=True,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Topic :: Scientific/Engineering :: Visualization',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
      ],
      )
