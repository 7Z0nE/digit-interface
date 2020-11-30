# Copyright (c) Facebook, Inc. and its affiliates. All rights reserved.
from __future__ import absolute_import
import os

import nox

BASE = os.path.abspath(os.path.dirname(__file__))

DEFAULT_PYTHON_VERSIONS = [u"3.7"]

LINT_SETUP_DEPS = [u"black", u"flake8", u"flake8-copyright", u"isort"]
DEPLOY_SETUP_DEPS = [u"twine"]

VERBOSE = os.environ.get(u"VERBOSE", u"0")
SILENT = VERBOSE == u"0"

USING_CI = os.environ.get(u"USING_CI", False)
PYPI_USERNAME = os.environ.get(u"PYPI_USERNAME", None)
PYPI_PASSWORD = os.environ.get(u"PYPI_PASSWORD", None)


def _base_install(session):
    session.install(u"--upgrade", u"setuptools", u"pip", silent=SILENT)


def install_lint_deps(session):
    _base_install(session)
    session.install(*LINT_SETUP_DEPS, silent=SILENT)


def install_deploy_deps(session):
    _base_install(session)
    session.install(*DEPLOY_SETUP_DEPS, silent=SILENT)


def install_pytouch(session):
    session.chdir(BASE)
    session.run(u"pip", u"install", u"-e", u".")


@nox.session(python=DEFAULT_PYTHON_VERSIONS)
def lint(session):
    install_lint_deps(session)
    session.run(u"black", u"--check", u".", silent=SILENT)
    session.run(
        u"isort", u"--check", u"--diff", u".", u"--skip=.nox", silent=SILENT,
    )
    session.run(u"flake8", u"--config", u".flake8")


@nox.session(python=DEFAULT_PYTHON_VERSIONS)
def tests(session):
    _base_install(session)
    install_pytouch(session)
    session.install(u"pytest")
    session.run(u"pytest", u"tests")


@nox.session(python=DEFAULT_PYTHON_VERSIONS)
def build(session):
    _base_install(session)
    session.run(u"rm", u"-rf", u"dist", external=True)
    session.run(u"python", u"setup.py", u"sdist")


@nox.session(python=DEFAULT_PYTHON_VERSIONS)
def deploy(session):
    if not USING_CI:
        session.skip(u"Skipping deployment to PyPi.")
    install_deploy_deps(session)
    session.run(
        u"twine",
        u"upload",
        u"dist/*",
        env={u"TWINE_USERNAME": PYPI_USERNAME, u"TWINE_PASSWORD": PYPI_PASSWORD},
    )
