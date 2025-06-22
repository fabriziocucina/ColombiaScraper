import yaml
from pathlib import Path

def load_config(country: str) -> dict:
    config_path = Path(__file__).parent / f"{country}_camara.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
