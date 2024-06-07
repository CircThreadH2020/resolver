from setuptools import setup

setup(
    name="resolver",
    version="0.0.2",
    url="http://github.com/CircThread/resolver",
    author="Jonas Brozeit, Leonhard Kunz",
    license="MIT",
    python_requires='>=3.6',
    install_requires=open("requirements.txt").read().splitlines()
)
