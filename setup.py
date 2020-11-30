# Copyright (c) Facebook, Inc. and its affiliates. All rights reserved.

# This source code is licensed under the license found in the LICENSE file in the root directory of this source tree.

from __future__ import with_statement
from __future__ import absolute_import
import os
import re

from setuptools import find_packages, setup
from io import open

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

install_requires = [u"numpy >= 1.16", u"opencv-python", u"pyudev"]

dependency_links = []


def read(fname):
    return open(os.path.join(BASE_DIR, fname)).read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(ur"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError(u"Unable to find version string.")


with open(u"README.md", u"r") as fh:
    long_description = fh.read()

setup(
    name=u"digit_interface",
    version=find_version(u"digit_interface/__init__.py"),
    description=u"Interface for the DIGIT tactile sensor.",
    url=u"https://github.com/facebookresearch/digit-interface",
    author=u"Mike Lambeta, Roberto Calandra",
    author_email=u"lambetam@fb.com, rcalandra@fb.com",
    keywords=[u"science"],
    long_description=long_description,
    long_description_content_type=u"text/markdown",
    license=u"LICENSE",
    packages=find_packages(),
    install_requires=install_requires,
    dependency_links=dependency_links,
    zip_safe=True,
    classifiers=[
        u"Programming Language :: Python :: 3",
        u"Operating System :: POSIX :: Linux",
    ],
    python_requires=u">=3.6",
)
