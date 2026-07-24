# Development Setup

## Architecture Rules

When developing or modifying this project, you must follow the
[project architecture rules](docs/rules/architecture.md).

## Prerequisites

Before setting up the development environment, install the following required
tools and make sure they are available in `PATH`:

- `uv` — Python package and environment manager
- `git` — version control system
- `openssl` — RSA key generation utility
- `just` — project command runner  [gh-docs](https://github.com/casey/just#packages)

Verify the installation:

```sh
uv --version
git --version
openssl version
just --version
```

[About just autocompletion](docs/about_just_autocomplete.md)


## Project Setup

```sh
just setup
```

## Local Configuration

After setup, copy any configuration files you need from `local` and remove the `.example` suffix:

- `local/justfile.example` → `local/justfile`
- `local/docker-compose.example.yml` → `local/docker-compose.yml`

These optional files are ignored by Git 
and can be customized for local development, debugging, experiments and tests.

Before deployment, 
switch to the production configuration
and test it in a production-like environment.
