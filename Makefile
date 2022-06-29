
# Make sure python v3.8+ and py38-sqlite3 (or higher ver) is installed before anything else

.PHONY: dev
dev:
	test -d devenv || python -m venv devenv

.PHONY: deps
deps:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

.PHONY: test
test:
	nose2 --with-coverage

.PHONY: coverage
coverage:
	coverage html

.PHONY: bench
bench:
	export PYTHONPATH=. && python tests/benchmark_opensimplex.py

.PHONY: lint
lint:
	pycodestyle --max-line-length 120 opensimplex

.PHONY: format
format:
	black --line-length 120 --extend-exclude "opensimplex\/constants\.py" opensimplex/ tests/

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
	rm -rf *.egg-info/
	rm -f noise2d.png noise3d.png noise4d.png README.html
	find ./ -iname '*.pyc' | xargs rm -f
	find ./ -iname '__pycache__' | xargs rm -rf
	rm -f .coverage
	rm -rf htmlcov/
