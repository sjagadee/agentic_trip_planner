import subprocess
import sys
import yaml


def load_packages(filepath: str = "packages.yaml") -> dict:
    with open(filepath) as f:
        return yaml.safe_load(f)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def install(packages: list[str], dev: bool = False) -> None:
    cmd = ["uv", "add"]
    if dev:
        cmd.append("--dev")
    run(cmd + packages)


if __name__ == "__main__":
    args = sys.argv[1:]
    dev = "--dev" in args
    yaml_file = next((a for a in args if a.endswith(".yaml")), "packages.yaml")

    packages = load_packages(yaml_file)

    if dev:
        install(packages.get("dev", []), dev=True)
    else:
        install(packages.get("dependencies", []))
        install(packages.get("dev", []), dev=True)

    run(["uv", "sync"])