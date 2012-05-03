PYTHON ?= python
NOSE ?= nosetests
PEP8 ?= pep8

CLEAN += build/ dist/

SETUP = $(PYTHON) setup.py

test: style
	$(NOSE)

upload: test
	$(SETUP) sdist upload

style:
	$(PEP8) src/ test/

clean:
	rm -rf $(CLEAN)
