import os
import yaml
from dotenv import load_dotenv
from types import SimpleNamespace


def _to_namespace(d):
    if isinstance(d, dict):
        return SimpleNamespace(**{k: _to_namespace(v) for k, v in d.items()})
    return d


class ConfigLoader:
    def __init__(self, config_path: str = None):
        load_dotenv()
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(__file__), "..", "config", "config.yaml"
            )
        with open(os.path.abspath(config_path), "r") as f:
            data = yaml.safe_load(f)
        for key, value in data.items():
            setattr(self, key, _to_namespace(value))
