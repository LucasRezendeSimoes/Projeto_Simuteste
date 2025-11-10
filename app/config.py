import yaml
from typing import Any, Dict

def load_config(path: str = "config.yaml") -> Dict[str, Any]:
    """Carrega arquivo de configuração YAML."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

CONFIG = load_config()
