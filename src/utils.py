"""
Fonctions utilitaires (logs, config, etc.)
"""
import yaml

def charger_config(path_yaml):
    """Charge le fichier de configuration YAML."""
    with open(path_yaml, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)
