"""
Module utilitaire fournissant les fonctions de base pour le projet de segmentation client.
"""

import os
import yaml
import logging
import pandas as pd
from datetime import datetime
from typing import Dict, Any

def load_config(path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Charge la configuration YAML et renvoie un dictionnaire Python.
    
    Args:
        path (str): Chemin vers le fichier de configuration
        
    Returns:
        Dict[str, Any]: Configuration sous forme de dictionnaire
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.error(f"Erreur lors du chargement de la configuration: {str(e)}")
        raise

def setup_logger(name: str = "project_logger", log_path: str = "logs/project.log") -> logging.Logger:
    """
    Initialise un logger avec format standard.
    
    Args:
        name (str): Nom du logger
        log_path (str): Chemin du fichier de log
        
    Returns:
        logging.Logger: Logger configuré
    """
    # Créer le dossier de logs s'il n'existe pas
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    # Configurer le logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '[%(levelname)s] [%(asctime)s] %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler fichier
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

def save_dataframe(df: pd.DataFrame, path: str) -> None:
    """
    Sauvegarde un DataFrame au format CSV.
    
    Args:
        df (pd.DataFrame): DataFrame à sauvegarder
        path (str): Chemin de sauvegarde
    """
    try:
        # Créer le dossier si nécessaire
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Sauvegarder le DataFrame
        df.to_csv(path, index=False, encoding='utf-8')
        logging.info(f"DataFrame sauvegardé avec succès: {path}")
    except Exception as e:
        logging.error(f"Erreur lors de la sauvegarde du DataFrame: {str(e)}")
        raise

def create_output_filename(base_name: str, extension: str = "csv") -> str:
    """
    Crée un nom de fichier unique avec timestamp.
    
    Args:
        base_name (str): Nom de base du fichier
        extension (str): Extension du fichier
        
    Returns:
        str: Nom de fichier unique
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}.{extension}"