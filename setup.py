from setuptools import setup, find_packages
from cache.version import __version__

setup(
    name="cache",
    version=__version__,
    description="caching for humans",
    author="Jay Adkisson",
    url="https://github.com/jayferd/python-cache",
    author_email="j4yferd at gmail dot com (humans only, please)",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Topic :: Database :: Front-Ends",
        "License :: OSI Approved :: MIT License",
    ],
    requires=["decorator"],
    keywords="cache decorator humans",
    packages=find_packages(),
)
