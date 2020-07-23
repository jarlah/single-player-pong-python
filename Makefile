.PHONY: test

default: docker

.PHONY: install
install:
	poetry install

.PHONY: lint
lint: install
	poetry run pre-commit run --all-files


test: lint install
	poetry run coverage run --source=kube_downscaler -m py.test -v
	poetry run coverage report
