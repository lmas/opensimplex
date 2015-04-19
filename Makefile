

build:
	python setup.py sdist
upload: build
	twine upload -r pypi dist/*
upload-test: build
	twine upload -r testpypi dist/*
test:
	 python -m opensimplex.tests.opensimplex_test
html:
	python setup.py --long-description | rst2html.py > README.html
clean:
	rm -rf dist/
	rm -rf opensimplex.egg-info/
	find ./ -iname '*.pyc' | xargs rm -f
	find ./ -iname '__pycache__' | xargs rm -rf
