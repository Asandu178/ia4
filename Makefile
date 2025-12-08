
PYTHON = python3
SRC_DIR = src
MAIN_SCRIPT = $(SRC_DIR)/main.py

.PHONY: run clean install

run:
	$(PYTHON) $(MAIN_SCRIPT)

install:
	pip install -r requirements.txt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
