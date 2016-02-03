PYTHON=python3
# TODO interactively select and check python version
test:
	$(PYTHON) -m unittest doan.test

upload:
	rm -rf dist
	python setup.py sdist bdist_wheel
	twine upload -u `keepassx.sh pypi username` -p `keepassx.sh pypi` dist/*
