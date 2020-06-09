setup:
	python3 -m venv ~/.ccdr

install:
	pip3 install -r requirements.txt --user

test:
	python -m pytest -vv --cov=app/lib tests/**.py

lint:
	export PYTHONPATH="./app" && \
	pylint --disable=R,C,W0703,W0101,E1101,W0613 app/

all: install lint test
