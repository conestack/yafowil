from setuptools import setup, find_packages
import os

version = '2.0'
shortdesc = \
'YAFOWIL - declarative, flexible html forms, framework independent.'
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'HISTORY.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.rst')).read()
tests_require = ['interlude', 'lxml']

setup(name='yafowil',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Software Development',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'License :: OSI Approved :: BSD License',
      ],
      keywords='html input widgets form compound',
      author='BlueDynamics Alliance',
      author_email='dev@bluedynamics.com',
      url=u'http://pypi.python.org/pypi/yafowil',
      license='Simplified BSD',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['yafowil'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'setuptools',
          'node',
      ],
      tests_require=tests_require,
      test_suite="yafowil.tests.test_suite",
      extras_require = dict(
          test=tests_require,
      ),
      entry_points = """
      [yafowil.plugin]
      register = yafowil.loader:register
      example = yafowil.example:get_example
      """,
)
