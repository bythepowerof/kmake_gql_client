#!/bin/bash

set -e -x

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
	echo Bootstrapping python 3.7.3 installation on osx ...
	# Inspired by: https://github.com/pyca/cryptography/blob/master/.azure-pipelines/macos-wheels.yml
	PYTHON_DOWNLOAD_URL="https://www.python.org/ftp/python/3.7.3/python-3.7.3-macosx10.6.pkg"
	PYTHON_BIN_PATH="/Library/Frameworks/Python.framework/Versions/3.7/bin/python3"
	curl -o python.pkg -L "$PYTHON_DOWNLOAD_URL"
	sudo installer -pkg python.pkg -target /
	"$PYTHON_BIN_PATH" -m pip install -U virtualenv
	"$PYTHON_BIN_PATH" -m virtualenv .venv
	source .venv/bin/activate
	pip install -U wheel
	echo finished bootstrapping.
fi

python -c 'import sys; print(sys.prefix)'

