SYS_PYTHON = $(shell which python3.12)
ENV_PYTHON = venv/bin/python3
REQUIREMENTS_TXT = requirements.txt
EXAMPLE_YAML = example_config.yaml
VROOM_YAML = vroom.yaml
RETCH_BIN = retch.py

.PHONY: init lint run all
all: init lint test

init: $(ENV_PYTHON)

run: example.rc example.gtkw

%.rc: %.yaml $(REQUIREMENTS_TXT)
	$(ENV_PYTHON) $(RETCH_BIN) $< -f rc $@

%.gtkw: %.yaml $(REQUIREMENTS_TXT)
	$(ENV_PYTHON) $(RETCH_BIN) $< -f gtkw $@

lint: $(REQUIREMENTS_TXT) $(EXAMPLE_YAML)
	$(ENV_PYTHON) -m mypy $(RETCH_BIN)
	$(ENV_PYTHON) -m mypy -p libretch

$(ENV_PYTHON): $(REQUIREMENTS_TXT)
	${SYS_PYTHON} -m venv venv
	. venv/bin/activate && pip install --upgrade pip && pip install -r $(REQUIREMENTS_TXT)

test:
	$(ENV_PYTHON) -m pytest
