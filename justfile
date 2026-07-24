
[windows]
set shell := ["powershell.exe", "-NoLogo", "-NoProfile", "-Command"]

[unix]
set shell := ["sh", "-uc"]

set default-list

import? 'local/local.just'

# Prepare the project for local development.
[group: "dev"]
setup:
    python prepare_project_dev.py

# Synchronize project dependencies.
[group: "dev"]
sync:
    uv sync

# Start the application.
[group: "dev"]
app:
    cd src && uv run python main.py



# -------Migration manager----------

# Generate a migration: just migrations "migration name"
[group: "migration"]
makemigrations message:
    cd src && uv run alembic -c setup/db/alembic.ini revision --autogenerate -m "{{ message }}"

#  Upgrade to a particular revision: just migrate +1 (default all)
[group: "migration"]
migrate revision="head":
    cd src && uv run alembic -c setup/db/alembic.ini upgrade {{revision}}

# Downgrade to a particular revision (default revert the latest migration) 
[group: "migration"]
downgrade revision="-1":
    cd src && uv run alembic -c setup/db/alembic.ini downgrade {{revision}}

# Show migration history.
[group: "migration"]
migration-history:
    cd src && uv run alembic -c setup/db/alembic.ini history

# Show the current database revision.
[group: "migration"]
migration-current:
    cd src && uv run alembic -c setup/db/alembic.ini current

# Check whether model changes require a migration.
[group: "migration"]
migration-check:
    cd src && uv run alembic -c setup/db/alembic.ini check

# ------Code quality--------

# Run Ruff checks.
[group: "code-quality"]
lint *flags:
    uv run ruff check {{flags}} .  

# Run Ruff checks with unsafe-fixes.
[group: "code-quality"]
unsafe-lint *flags:
    uv run ruff check --unsafe-fixes {{flags}} .  

# Run Ruff format 
[group: "code-quality"]
format *flags: 
    uv run ruff format . {{flags}}

# Run static type checking.
[group: "code-quality"]
typecheck:
    uv run pyright src

# Apply formatting and safe automatic fixes.
[group: "code-quality"]
fix: (lint "--fix") format 

# Run the main local/CI verification suite.
[group: "code-quality"]
check: (format "--check") lint typecheck migration-check
    


# --Docker--

# Up containers
[group: "docker"]
docker-up *args:
    docker compose up -d {{args}} 

#Build containers
[group: "docker"]
docker-build *args:
    docker compose build {{args}} 

# Stop and remove  containers.
[group: "docker"]
docker-down *args:
    docker compose down {{args}}

# Follow logs for services.
[group: "docker"]
docker-logs *args:
    docker compose logs --follow --tail=200 {{args}}

# Open a shell inside the application container.
[group: "docker"]
docker-shell service:
    docker compose exec -it {{service}} sh