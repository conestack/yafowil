# Copyright 2009, BlueDynamics Alliance - http://bluedynamics.com
# Python Software Foundation License

from setuptools import setup, find_packages
import sys, os

version = '1.1'
shortdesc = \
'YAFOWIL - Yet Another Form Widget Lib: Lightweight, Extensible, Pluggable, Pure.'
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'HISTORY.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.rst')).read()

tests_require = ['interlude', 'lxml']

setup(name='yafowil',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'License :: OSI Approved :: Python Software Foundation License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Software Development',
      ],
      keywords='html input widgets form compound array',
      author='BlueDynamics Alliance',
      author_email='dev@bluedynamics.com',
      url=u'https://github.com/bluedynamics/yafowil',
      license='BSD simplified',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['yafowil'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'setuptools',
          'zodict',
      ],
      tests_require=tests_require,
      test_suite="yafowil.tests.test_suite",
      extras_require = dict(
          test=tests_require,
      ),
)
