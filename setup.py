from setuptools import find_packages
from setuptools import setup
from setuptools.command.test import test
import os


def read_file(name):
    with open(os.path.join(os.path.dirname(__file__), name)) as f:
        return f.read()


version = '2.3.4'
shortdesc = 'YAFOWIL - declarative, framework independent, flexible HTML forms'
longdesc = '\n\n'.join([read_file(name) for name in [
    'README.rst',
    'CHANGES.rst',
    'LICENSE.rst'
]])


class Test(test):

    def run_tests(self):
        from yafowil import tests
        tests.run_tests()


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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='html input widgets form compound',
    author='Yafowil Contributors',
    author_email='dev@conestack.org',
    url=u'http://github.com/conestack/yafowil',
    license='Simplified BSD',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['yafowil'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'node>=0.9.28',
        'plumber>=1.3',
    ],
    tests_require=[
        'lxml',
        'zope.testrunner'
    ],
    test_suite='yafowil.tests.test_suite',
    extras_require=dict(test=[
        'lxml',
        'zope.testrunner'
    ]),
    entry_points="""
    [yafowil.plugin]
    register = yafowil.loader:register
    example = yafowil.example:get_example
    """
)
