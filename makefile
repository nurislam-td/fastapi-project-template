.PHONY: app sync setup migrations migrate downgrade

-include local/makefile

app:
	cd src && uv run python main.py 

sync: 
	uv sync 

setup:
	python prepare_project_dev.py


# make migrations m='name'
migrations:
	cd src && uv run alembic -c setup/db/alembic.ini revision --autogenerate -m '$(m)'

migrate: 
	cd src && uv run alembic -c setup/db/alembic.ini upgrade head 

downgrade: 
	cd src && uv run alembic -c setup/db/alembic.ini downgrade head -1

