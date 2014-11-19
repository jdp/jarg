import os

from setuptools import setup

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

dist = setup(
    name='jarg',
    version='0.1.0',
    license='MIT',
    description="A shorthand JSON syntax for your shell",
    long_description=readme,
    classifiers=classifiers,
    author="Justin Poliey",
    author_email="justin.d.poliey@gmail.com",
    url='http://github.com/jdp/jarg',
    include_package_data=True,
    zip_safe=False,
    py_modules=['jarg'],
    entry_points={
        'console_scripts': ['jarg = jarg:main'],
    },
)