if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
	source .venv/bin/activate
fi

python -c 'import sys; print(sys.prefix)'
