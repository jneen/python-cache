PYTHON ?= python
NOSE ?= nosetests
PEP8 ?= pep8

CLEAN += build/ dist/

SETUP = $(PYTHON) setup.py

upload:
	$(SETUP) sdist upload

test: style
	$(NOSE)

style:
	$(PEP8) src/ test/

clean:
	rm -rf $(CLEAN)
