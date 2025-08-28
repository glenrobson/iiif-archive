import os
# read the contents of your README file
from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

if os.path.exists("version.txt"):
    VERSION = (this_directory / "version.txt").read_text().strip()
else:
    VERSION = "0.0.0.dev0"

REQUIREMENTS = [
    "requests >=2.28.0, <3.0.0"
]

DOCS_REQUIREMENTS = [
]

DEV_REQUIREMENTS = [
    "autopep8 >=1.6.0, <3.0.0",
    "isort >=5.10.1, <6.0.0",
    "flake8 >=7.2.0, <8.0.0",
    "flake8-docstrings >=1.6.0, <2.0.0",
    "flake8-isort >=4.1.1, <7.0.0",
    "tox >=3.25.0, <5.0.0"
]

# Setting up
setup(
    name="iiif-archive",
    version=VERSION,
    author="Glen Robson",
    description="Download a IIIF Manifest and store in a zip file.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['iiif_archive'],
    classifiers=["Development Status :: 5 - Production/Stable",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: Apache Software License",
                 "Operating System :: OS Independent",  # is this true? know Linux & OS X ok
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.9",
                 "Programming Language :: Python :: 3.10",
                 "Programming Language :: Python :: 3.11",
                 "Programming Language :: Python :: 3.12",
                 "Programming Language :: Python :: 3.13",
                 "Topic :: Internet :: WWW/HTTP",
                 "Topic :: Multimedia :: Graphics :: Graphics Conversion",
                 "Topic :: Software Development :: Libraries :: Python Modules",
                 "Environment :: Web Environment"],
    python_requires='>=3',
    url='https://github.com/glenrobson/iiif-archive',
    license='MIT License',
    install_requires=REQUIREMENTS,
    extras_require={
        "docs": DOCS_REQUIREMENTS,
        "dev": DEV_REQUIREMENTS,
    },
)
