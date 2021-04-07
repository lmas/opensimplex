
.PHONY: test
test:
	nosetests --with-coverage --cover-package=opensimplex tests/

.PHONY: bench
bench:
	export PYTHONPATH=. && python tests/benchmark_opensimplex.py

.PHONY: format
format:
	autopep8 --aggressive --aggressive --max-line-length 120 --in-place --recursive opensimplex

.PHONY: lint
lint:
	pycodestyle opensimplex

.PHONY: test
build: test
	python setup.py sdist bdist_wheel

.PHONY: upload
upload:
	twine upload -r pypi dist/*

.PHONY: upload-test
upload-test:
	twine upload -r testpypi dist/*

.PHONY: clean
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf opensimplex.egg-info/
	rm -f noise2d.png noise3d.png noise4d.png README.html
	rm -f .coverage
	find ./ -iname '*.pyc' | xargs rm -f
	find ./ -iname '__pycache__' | xargs rm -rf
