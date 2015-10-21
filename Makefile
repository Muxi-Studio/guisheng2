# guisheng project makefile
.PHONY: test clean-pyc

# run unit test
test:
	python manage.py test --coverage

# clean *pyc, *pyo
clean-pyc:
	find . -name '*.pyc' -exec rm -rf {} +
	find . -name '*.pyo' -exec rm -rf {} +

