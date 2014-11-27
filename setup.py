import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

import jarg


here = os.path.abspath(os.path.dirname(__file__))
readme = open(os.path.join(here, 'README.rst')).read()

classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Internet',
    'Topic :: Utilities',
]


class PyTest(TestCommand):
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


dist = setup(
    name='jarg',
    version='.'.join(jarg.__VERSION__),
    license='MIT',
    description="A shorthand encoding syntax for your shell",
    long_description=readme,
    classifiers=classifiers,
    author="Justin Poliey",
    author_email="justin.d.poliey@gmail.com",
    url='http://github.com/jdp/jarg',
    include_package_data=True,
    zip_safe=False,
    packages=['jarg'],
    entry_points={
        'console_scripts': ['jarg = jarg:main'],
    },
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},
)
