"""
setup.py

Resource for setting up testing: http://doc.pytest.org/en/latest/goodpractices.html
"""

import os
import re
import wheel
from setuptools import setup
from setuptools.command.test import test as TestCommand

os.environ['FALCON_HOME'] = os.getcwd()

# Utility function to read README file contents.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.initialize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import shlex
        # import here, because outside the eggs aren't loaded
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)

def recurse_falcon_libs():
    """
    Because setuptools (or distutils?) refuses to do recursive globbing AFAICT.

    Returns:
        list: allllll the directories and udfalcon/graderlib.
    """
    a = []

    for root, dirs, files in os.walk('udfalcon/graderlib'):
        # the [9:] gets rid of 'udfalcon/' at the beginning, which isn't
        # necessary because it's specified for the falcon package.
        if not 'docs' in root:
            a += [(os.path.join(root, d) + '/*')[9:] for d in dirs if not 'docs' in d]
    return a

setup(
    name = 'falcon',
    version = '0.3.1',
    author = 'Udacity',
    author_email = 'cameron@udacity.com',
    description = ('Python middleware for REX programming quizzes.'),
    license = 'MIT',
    keywords = 'udacity middleware rex',
    url = 'https://github.com/udacity/falcon',
    packages = ['udfalcon'],
    package_data={
        'udfalcon': recurse_falcon_libs()
    },
    long_description = read('README.md'),
    setup_requires = ['pytest-runner'],
    tests_require = ['pytest'],
    test_suite = 'falcon.test',
    cmdclass = {'test': PyTest},
    entry_points = {
        "console_scripts": [
            'falcon = udfalcon.__main__:main'
        ]
    },
    platforms = 'any',
    classifiers = [
        'Programming Language :: Python :: 3.4',
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
