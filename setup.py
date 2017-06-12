import os
from setuptools import setup
from setuptools import find_packages


def read_file(name):
    with open(os.path.join(os.path.dirname(__file__), name)) as f:
        return f.read()


version = '2.2.3'
shortdesc = 'YAFOWIL - declarative, framework independent, flexible HTML forms'
longdesc = '\n\n'.join([read_file(name) for name in [
    'README.rst',
    'CHANGES.rst',
    'LICENSE.rst'
]])
tests_require = ['interlude', 'lxml']


setup(
    name='yafowil',
    version=version,
    description=shortdesc,
    long_description=longdesc,
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='html input widgets form compound',
    author='BlueDynamics Alliance',
    author_email='dev@bluedynamics.com',
    url=u'http://pypi.python.org/pypi/yafowil',
    license='Simplified BSD',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['yafowil'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'node>0.9.10',
        'plumber>=1.3',
    ],
    tests_require=tests_require,
    test_suite="yafowil.tests.test_suite",
    extras_require=dict(
        test=tests_require,
    ),
    entry_points="""
    [yafowil.plugin]
    register = yafowil.loader:register
    example = yafowil.example:get_example
    """)
