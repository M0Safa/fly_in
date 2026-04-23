PYTHON = python3
MAIN   =fly_in.py
MAP = "maps/medium/03_priority_puzzle.txt"

install:
		pip install -r requirement.txt

run:
		$(PYTHON) $(MAIN) $(MAP)

debug:
		$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
		find . -type d -name "__pycache__" -exec rm -rf {} +
		rm -rf .mypy_cache

lint:
		flake8 .
		mypy . \
				--warn-return-any \
				--warn-unused-ignores \
				--ignore-missing-imports \
				--disallow-untyped-defs \
				--check-untyped-defs

.PHONY: install run debug clean lint(venv)