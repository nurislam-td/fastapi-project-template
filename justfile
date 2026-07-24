
[windows]
set shell := ["powershell.exe", "-NoLogo", "-NoProfile", "-Command"]

[unix]
set shell := ["sh", "-uc"]

set default-list

import? 'local/justfile'

# Prepare the project for local development.
setup:
    python prepare_project_dev.py


# Start the application.
app:
    cd src && uv run python main.py

# Synchronize project dependencies.
sync:
    uv sync

# Generate a migration: just migrations "migration name"
makemigrations message:
    cd src && uv run alembic -c setup/db/alembic.ini revision --autogenerate -m "{{ message }}"

# Apply all pending migrations.
migrate:
    cd src && uv run alembic -c setup/db/alembic.ini upgrade head

# Revert the latest migration.
downgrade:
    cd src && uv run alembic -c setup/db/alembic.ini downgrade head -1


# Run Ruff checks.
lint *flags:
    uv run ruff check {{flags}} .  

# Run Ruff checks.
unsafe-lint *flags:
    uv run ruff check --unsafe-fixes {{flags}} .  



# Run Ruff format 
format *flags: 
    uv run ruff format . {{flags}}
