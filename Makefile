setup:
	python3 -m venv ~/.ccdr

install:
	pip3 install -r requirements.txt

test:
	python -m pytest -vv --cov=app-automl/lib tests/automl/**.py && \
    python -m pytest -vv --cov=app-keras/lib tests/keras/**.py

automl-lint:
	export PYTHONPATH="./app-automl" && \
	pylint --disable=R,C,W0703,W0101,E1101,W0613 app-automl/

keras-lint:
	export PYTHONPATH="./app-keras" && \
	pylint --disable=R,C,W0703,W0101,E1101,W0613,W0611,E0401 app-keras/

lint: automl-lint keras-lint

all: install lint test
