exe:
	python dicemodel.py
doc:
	epydoc --html -o doc -name OWNDICE *.py
pylint:
	pylint dicemodel.py
test:
	python -m unittest discover
clean:
	rm -rf doc
	rm *.pyc
