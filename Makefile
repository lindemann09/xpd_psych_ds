.PHONY: install clean build

install:
	python3 setup.py install

build:
	python3 setup.py sdist bdist_wheel 

publish:
	twine check dist/*	
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

clean:
		@rm -rf build \
			dist \
			xpd_to_psych_ds.egg-info \
