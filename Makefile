PIP = pip
TEST_DIR = tests
PRJ = postmin
PYTEST_FLAGS = -v


.PHONY: env-py
env-py:
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .


.PHONY: env-node
env-node:
	npm install


.PHONY: env
env: env-py env-node


.PHONY: lint-py
lint-py:
	flake8


.PHONY: lint-node
lint-node:
	npm run lint


.PHONY: lint
lint: lint-py lint-node


.PHONY: serve
serve:
	npm run dev

########################


.PHONY: test
test:
	pytest $(PYTEST_FLAGS) $(TEST_DIR)


.PHONY: cover
cover:
	pytest $(PYTEST_FLAGS) --cov=$(PRJ) $(TEST_DIR)


.PHONY: sdist
sdist:
	python3 setup.py sdist


.PHONY: bdist
bdist:
	python3 setup.py bdist_egg


.PHONY: dist
dist: sdist bdist
