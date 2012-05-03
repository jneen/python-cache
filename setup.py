from setuptools import setup, find_packages

from os.path import join, dirname
import sys
sys.path.insert(0, join(dirname(__file__), 'src'))
from cache.version import __version__
sys.path.pop(0)

setup(
    name="cache",
    version=__version__,
    description="caching for humans",
    author="Jay Adkisson",
    url="https://github.com/jayferd/python-cache",
    author_email="j4yferd at gmail dot com (humans only, please)",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Topic :: Database :: Front-Ends",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="cache decorator humans",
    packages=find_packages('src'),
    package_dir={'': 'src'},
)
