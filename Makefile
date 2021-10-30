
.PHONY: deps
deps:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

.PHONY: test
test:
	export NUMBA_DISABLE_JIT=1 && nosetests --with-coverage --cover-package=opensimplex tests/test_opensimplex.py

.PHONY: bench
bench:
	export PYTHONPATH=. && python tests/benchmark_opensimplex.py

.PHONY: format
format:
	autopep8 --aggressive --aggressive --max-line-length 120 --in-place --recursive --verbose opensimplex

.PHONY: lint
lint:
	pycodestyle --max-line-length 120 opensimplex

.PHONY: build
build: test
	python setup.py sdist bdist_wheel

.PHONY: upload
upload: build
	twine upload -r pypi dist/*

.PHONY: upload-test
upload-test: build
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
