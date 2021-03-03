.ONESHELL:
.PHONY: docs

debug:
	pip install . --force --no-deps

install:
	poetry install

mypy:
	mypy pytezos

lint: mypy

test:
	pytest -v .

docs:
	cd docs && rm -rf ./build && $(MAKE) html

rpc-docs:
	python -m scripts.fetch_docs

release-patch:
	bumpversion patch
	git push --tags
	git push

release-minor:
	bumpversion minor
	git push --tags
	git push

release-major:
	bumpversion major
	git push --tags
	git push