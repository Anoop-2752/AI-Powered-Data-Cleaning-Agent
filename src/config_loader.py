import yaml
import os

def load_cleaning_config(config_path="config/cleaning_rules.yaml"):
    if not os.path.exists(config_path):
        print(f"⚠️ Config file not found at {config_path}, using defaults.")
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
