"""
Module utilitaire
Fonctions helpers communes
"""
import pandas as pd
import yaml
def load_config():
    """Chargement de la configuration YAML"""
    with open('config/config.yaml', 'r') as file:
        return yaml.safe_load(file)



def format_currency(value):
    """Formatage des montants en £"""
    return f"£{value:,.2f}"

def safe_qcut(series, q, labels):
    """qcut sécurisé"""
    try:
        return pd.qcut(series, q, labels=labels, duplicates='drop')
    except ValueError:
        return pd.Series([labels[0]] * len(series))