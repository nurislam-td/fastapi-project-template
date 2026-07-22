from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

ENV_TEMPLATE = PROJECT_ROOT / ".env.local.example"
ENV_FILE = PROJECT_ROOT / ".env"
GIT_HOOKS_DIR = PROJECT_ROOT / ".githooks"
JWT_KEYS_DIR = PROJECT_ROOT / "src" / "crypt" / "jwt"
JWT_KEY_PAIRS = (
    (JWT_KEYS_DIR / "access_private.pem", JWT_KEYS_DIR / "access_public.pem"),
    (JWT_KEYS_DIR / "refresh_private.pem", JWT_KEYS_DIR / "refresh_public.pem"),
)


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


def generate_rsa_key_pair(private_path: Path, public_path: Path) -> None:
    if private_path.exists() and public_path.exists():
        key_pair_name = private_path.stem.removesuffix("_private")
        print(f"RSA key pair {key_pair_name} already exists and was left unchanged.")
        return

    if private_path.exists() or public_path.exists():
        print(
            f"Error: incomplete RSA key pair: {private_path} / {public_path}.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    with tempfile.TemporaryDirectory(dir=JWT_KEYS_DIR) as temporary_dir:
        temporary_path = Path(temporary_dir)
        temporary_private_path = temporary_path / private_path.name
        temporary_public_path = temporary_path / public_path.name

        run(
            "openssl",
            "genpkey",
            "-algorithm",
            "RSA",
            "-pkeyopt",
            "rsa_keygen_bits:2048",
            "-out",
            str(temporary_private_path),
        )
        run(
            "openssl",
            "pkey",
            "-in",
            str(temporary_private_path),
            "-pubout",
            "-out",
            str(temporary_public_path),
        )

        temporary_private_path.chmod(0o600)
        temporary_public_path.chmod(0o644)
        temporary_private_path.replace(private_path)
        temporary_public_path.replace(public_path)

    print(f"Created RSA key pair {private_path.stem.removesuffix('_private')}.")


def generate_jwt_keys() -> None:
    JWT_KEYS_DIR.mkdir(parents=True, exist_ok=True)
    for private_path, public_path in JWT_KEY_PAIRS:
        generate_rsa_key_pair(private_path, public_path)


def make_git_hooks_executable() -> None:
    if not GIT_HOOKS_DIR.is_dir():
        print(f"Error: {GIT_HOOKS_DIR} was not found.", file=sys.stderr)
        raise SystemExit(1)

    for hook_path in GIT_HOOKS_DIR.iterdir():
        if hook_path.is_file():
            hook_path.chmod(hook_path.stat().st_mode | 0o111)

    print("Git hooks were made executable.")


def main() -> None:
    require_command("uv")
    require_command("git")
    require_command("openssl")

    if not ENV_TEMPLATE.is_file():
        print(f"Error: {ENV_TEMPLATE.name} was not found.", file=sys.stderr)
        raise SystemExit(1)

    if ENV_FILE.exists():
        print("The .env file already exists and was left unchanged.")
    else:
        shutil.copy2(ENV_TEMPLATE, ENV_FILE)
        print("Created the .env file.")

    run("uv", "sync")
    make_git_hooks_executable()
    run("git", "config", "--local", "core.hooksPath", ".githooks")
    generate_jwt_keys()

    print("Project setup completed successfully.")


if __name__ == "__main__":
    main()
