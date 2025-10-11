"""
Module de nettoyage des données clients.
"""
import pandas as pd

def nettoyer_donnees(path_csv):
    """Charge et nettoie les données brutes."""
    df = pd.read_csv(path_csv)
    # 1. Suppression des transactions annulées
    # 2. Suppression des CustomerID manquants
    # 3. Filtrage des valeurs négatives
    # 4. Normalisation du texte
    # 5. Calcul du TotalPrice
    # 6. Export du dataset nettoyé
    return df
