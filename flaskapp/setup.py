import codecs
import os
import re
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


# Read the version number from a source file.
# Why read it, and not import?
# see https://groups.google.com/d/topic/pypa-dev/0PkjVpcxTzQ/discussion
def find_version(*file_paths):
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as h:
        version_file = h.read()

    # The version line must have the form
    # __version__='ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='lapiz',
    version=find_version('lapiz', '__init__.py'),

    description='Lapiz server',

    author='bosr',
    author_email='romain.bossart@fastmail.com',
    url='https://github.com/bosr/lapiz',

    install_requires=[
        "requests",
        "flask"
    ],

    packages=find_packages(),
    package_data={},

    entry_points={
        'console_scripts': []
    }
)
