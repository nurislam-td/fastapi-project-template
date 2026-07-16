.PHONY: app sync setup

-include local/makefile

app:
	cd src && uv run python main.py 

sync: 
	uv sync 

setup:
	python prepare_project_dev.py

