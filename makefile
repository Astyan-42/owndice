exe:
	python dicemodel.py
doc:
	epydoc --html --name "OWNDICE" -v -o doc *.py
pylint:
	pylint dicemodel.py
test:
	python -m unittest discover
clean:
	rm -rf doc
	rm *.pyc
