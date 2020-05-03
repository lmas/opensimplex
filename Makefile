
test:
	nosetests --with-coverage --cover-package=opensimplex tests/

benchmark:
	export PYTHONPATH=. && python tests/benchmark_opensimplex.py

codestyle:
	pycodestyle opensimplex

build: test
	python setup.py sdist

upload:
	twine upload -r pypi dist/*

upload-test:
	twine upload -r testpypi dist/*

clean:
	rm -rf dist/
	rm -rf opensimplex.egg-info/
	rm -f noise2d.png noise3d.png noise4d.png README.html
	rm -f .coverage
	find ./ -iname '*.pyc' | xargs rm -f
	find ./ -iname '__pycache__' | xargs rm -rf
