"""
setup.py

Resource for setting up testing: http://doc.pytest.org/en/latest/goodpractices.html
"""

import os
from setuptools import setup
from setuptools.command.test import test as TestCommand

# Utility function to read the README file.
# Used for the long_description. It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def finalize_options(self):
        TestCommand.initialize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import shlex
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)

setup(
    name = 'Falcon',
    version = '0.0.2',
    author = 'Udacity',
    author_email = 'jarrod@udacity.com',
    description = ('Python middleware for REX programming quizzes.'),
    license = 'MIT',
    keywords = 'udacity middleware rex',
    url = 'https://github.com/udacity/falcon',
    packages = ['falcon', 'test'],
    long_description = read('README.md'),
    setup_requires = ['pytest-runner'],
    tests_require = ['pytest'],
    test_suite = 'falcon.test.test_falcon',
    cmdclass = {'test': PyTest},
    platforms = 'any',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)