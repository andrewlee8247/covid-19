setup:
	python3 -m venv ~/.ccdr

install:
	pip3 install -r requirements.txt --user

test:
	python -m pytest -vv --cov=app/api/lib tests/**.py

lint:
	export PYTHONPATH="./app/api" && \
	pylint --disable=R,C,W0703,W0101,E1101 app/

all: install lint test
