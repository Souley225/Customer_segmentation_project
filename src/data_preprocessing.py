"""
Module de prétraitement des données pour le projet de segmentation client.
"""

import pandas as pd
import logging
from typing import Dict, Any
from datetime import datetime
from .utils import save_dataframe

logger = logging.getLogger(__name__)

def clean_data(config: Dict[str, Any]) -> pd.DataFrame:
    """
    Nettoie les données brutes et renvoie un DataFrame propre.
    
    Args:
        config (Dict[str, Any]): Configuration du projet
        
    Returns:
        pd.DataFrame: DataFrame nettoyé
    """
    logger.info("Début du nettoyage des données")
    
    try:
        # Charger les données brutes
        df = pd.read_csv(config["paths"]["raw_data"])
        initial_shape = df.shape
        logger.info(f"Données chargées: {initial_shape[0]} lignes, {initial_shape[1]} colonnes")
        
        # Supprimer les lignes avec quantité ou prix unitaire négatifs/nuls
        df = df[
            (df["Quantity"] > 0) & 
            (df["UnitPrice"] > 0)
        ]
        
        # Calculer le prix total
        df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
        
        # Supprimer les lignes sans CustomerID
        df = df.dropna(subset=["CustomerID"])
        
        # Convertir CustomerID en entier
        df["CustomerID"] = df["CustomerID"].astype(int)
        
        # Convertir la date
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
        
        # Sauvegarder les données nettoyées
        save_dataframe(df, config["paths"]["processed_data"])
        
        final_shape = df.shape
        logger.info(f"""Nettoyage terminé:
            - Lignes initiales: {initial_shape[0]}
            - Lignes finales: {final_shape[0]}
            - Colonnes: {final_shape[1]}""")
        
        return df
        
    except Exception as e:
        logger.error(f"Erreur lors du nettoyage des données: {str(e)}")
        raise

def validate_data(df: pd.DataFrame) -> bool:
    """
    Valide la qualité des données nettoyées.
    
    Args:
        df (pd.DataFrame): DataFrame à valider
        
    Returns:
        bool: True si les données sont valides
    """
    try:
        # Vérifier qu'il n'y a pas de valeurs négatives
        assert (df["Quantity"] > 0).all(), "Quantités négatives détectées"
        assert (df["UnitPrice"] > 0).all(), "Prix unitaires négatifs détectés"
        assert (df["TotalPrice"] > 0).all(), "Prix totaux négatifs détectés"
        
        # Vérifier que les CustomerID sont uniques par transaction
        assert df.groupby("InvoiceNo")["CustomerID"].nunique().max() == 1, \
            "Plusieurs clients pour une même facture"
        
        # Vérifier la cohérence des dates
        assert df["InvoiceDate"].max() <= datetime.now(), \
            "Dates futures détectées"
        
        logger.info("Validation des données réussie")
        return True
        
    except AssertionError as e:
        logger.error(f"Échec de la validation: {str(e)}")
        return False