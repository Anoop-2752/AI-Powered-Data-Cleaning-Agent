import os
import yaml
import json

CONFIG_PATH = os.path.join("config", "cleaning_rules.yaml")

def load_cleaning_config():
    """
    Loads cleaning configuration from YAML or JSON.
    """
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        if CONFIG_PATH.endswith(".yaml") or CONFIG_PATH.endswith(".yml"):
            return yaml.safe_load(f)
        elif CONFIG_PATH.endswith(".json"):
            return json.load(f)
        else:
            raise ValueError("Unsupported config format. Use YAML or JSON.")
