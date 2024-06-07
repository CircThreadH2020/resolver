[![Python Package](https://github.com/CircThread/resolver/actions/workflows/python-package.yml/badge.svg)](https://github.com/CircThread/resolver/actions/workflows/python-package.yml)
[![codecov](https://codecov.io/gh/CircThread/resolver/branch/master/graph/badge.svg)](https://codecov.io/gh/CircThread/resolver)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# resolver

My personal python starter template. Intended for copy and paste use. 

This project is released into the public domain, so feel free to modify and use it as you wish.

## Usage

### Copy files into your new project

Copy all files from this repository into your personal project. 

```bash
git clone https://github.com/CircThread/resolver.git tmp
rm -rf tmp/.git
cp -r tmp/.coveragerc tmp/.flake8 tmp/.gitignore tmp/* .
cp -r tmp/.github .github
rm -rf tmp
```

**Note**: If your project is not empty, it might overwrite your files.

### Adjust package name

Replace all occurrences of ```resolver``` and ```resolver``` with your package name.

You can do this for instance by first declaring a variable ```NEW_PROJECT_NAME``` and replacing ```<YOUR_PACKAGE_NAME>``` with your desired package/project name.

```bash
NEW_PROJECT_NAME=<YOUR_PACKAGE_NAME>
```

You can then use this variable to rename all occurrences in the template with your desired package/project name.

```bash
mv resolver $NEW_PROJECT_NAME
sed -i "s/resolver/$NEW_PROJECT_NAME/g" setup.py .coveragerc README.md "${NEW_PROJECT_NAME}/__main__.py" tests/test_core.py
sed -i "s/resolver/$NEW_PROJECT_NAME/g" README.md setup.py
```

### Adjust GitHub Username

If your username is not ```CircThread``` then you can first setup a new variable:

```bash
YOUR_GH_USERNAME=<YOUR_GITHUB_USERNAME>
```

Then you can replace it with the following command:

```bash
sed -i "s/CircThread/$YOUR_GH_USERNAME/g" setup.py README.md
```

### Adjust license

Replace the LICENSE file and change the ```license=Unlicense``` entry in ```setup.py``` to whatever you want to use. 
I would suggest the MIT license.

### Adjust author 

Also replace the author name in ```setup.py``` with your name.

### Adjust README.md

Adapt README.md, especially the installation instructions, according to your project. 

In particular, delete all the text up until **## Installation**

## Installation

```bash
pip install --user git+https://github.com/CircThread/resolver
```

## Usage

```bash
resolver
```

## Development

```bash
git clone https://github.com/CircThread/resolver
cd resolver
python -m venv venv
. venv/bin/activate
pip install -e .
pip install -r testing-requirements.txt
```

### Testing

```bash
pytest
```
