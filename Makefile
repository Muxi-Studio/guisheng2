# guisheng project makefile
.PHONY: test clean-testdb clean-pyc

# this makefile want to
all: test clean-testdb clean-pyc

# run unit test
test:
	python manage.py test --coverage

clean-testdb:
	rm -rf ./data-test.sqlite

# clean *pyc, *pyo
clean-pyc:
	find . -name '*.pyc' -exec rm -rf {} +
	find . -name '*.pyo' -exec rm -rf {} +
