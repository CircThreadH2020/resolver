import codecs
import os
import re

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="DOM_resolver",
    version=find_version("DOM_resolver", "__init__.py"),
    url="http://github.com/CircThread/DOM_resolver",
    author="Jonas Brozeit, Leonhard Kunz",
    license="MIT",
    python_requires='>3.6',
    packages=["DOM_resolver"],
    install_requires=[],
    entry_points={"console_scripts": ["DOM_resolver=DOM_resolver.__main__:main"]},
)
