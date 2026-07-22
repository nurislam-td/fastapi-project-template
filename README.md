# Development Setup

## Prerequisites

Before setting up the development environment, install the following required
tools and make sure they are available in `PATH`:

- `uv` — Python package and environment manager
- `git` — version control system
- `openssl` — RSA key generation utility

Verify the installation:

```sh
uv --version
git --version
openssl version
```

Installing GNU Make is recommended before working with the project. Make provides short, consistent commands for common tasks such as project setup, dependency synchronization, application startup, and testing. It also keeps implementation details in one shared place, so every developer can run the same workflows without having to remember long commands.

After installing it, verify that Make is available:

```sh
make --version
```

## Project Setup

```sh
make setup
```

## Local Configuration

After setup, copy any configuration files you need from `local` and remove the `.example` suffix:

- `local/makefile.example` → `local/makefile`
- `local/docker-compose.example.yml` → `local/docker-compose.yml`

These optional files are ignored by Git 
and can be customized for local development, debugging, experiments and tests.

Before deployment, 
switch to the production configuration
and test it in a production-like environment.
