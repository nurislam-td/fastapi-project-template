from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

ENV_TEMPLATE = PROJECT_ROOT / ".env.local.example"
ENV_FILE = PROJECT_ROOT / ".env"


def require_command(command: str) -> None:
    if shutil.which(command) is None:
        print(
            f"Error: {command} is not installed or is not available in PATH.",
            file=sys.stderr,
        )
        raise SystemExit(1)


def run(*command: str) -> None:
    print(f"> {' '.join(command)}", flush=True)
    result = subprocess.run(command, cwd=PROJECT_ROOT, check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> None:
    require_command("uv")
    require_command("git")

    if not ENV_TEMPLATE.is_file():
        print(f"Error: {ENV_TEMPLATE.name} was not found.", file=sys.stderr)
        raise SystemExit(1)

    if ENV_FILE.exists():
        print("The .env file already exists and was left unchanged.")
    else:
        shutil.copy2(ENV_TEMPLATE, ENV_FILE)
        print("Created the .env file.")

    run("uv", "sync")
    run("git", "config", "--local", "core.hooksPath", ".githooks")

    print("Project setup completed successfully.")


if __name__ == "__main__":
    main()
