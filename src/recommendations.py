"""
Module de génération de recommandations produits personnalisées.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Set
from collections import defaultdict
import logging
from .utils import save_dataframe

logger = logging.getLogger(__name__)

def get_customer_purchases(data: pd.DataFrame, customer_id: int) -> Set[str]:
    """
    Récupère l'ensemble des produits achetés par un client.
    
    Args:
        data (pd.DataFrame): Données nettoyées
        customer_id (int): ID du client
        
    Returns:
        Set[str]: Ensemble des produits achetés
    """
    return set(data[data["CustomerID"] == customer_id]["Description"].unique())

def get_similar_customers(rfm_df: pd.DataFrame, customer_id: int, n: int = 5) -> List[int]:
    """
    Trouve les clients similaires basés sur le segment RFM.
    
    Args:
        rfm_df (pd.DataFrame): Données RFM avec clusters
        customer_id (int): ID du client
        n (int): Nombre de clients similaires à retourner
        
    Returns:
        List[int]: Liste des IDs des clients similaires
    """
    # Obtenir le cluster du client
    customer_cluster = rfm_df[rfm_df["CustomerID"] == customer_id]["Cluster"].iloc[0]
    
    # Trouver les clients similaires du même cluster
    similar_customers = rfm_df[
        (rfm_df["Cluster"] == customer_cluster) & 
        (rfm_df["CustomerID"] != customer_id)
    ]["CustomerID"].tolist()
    
    return similar_customers[:n]

def get_recommendations_from_rules(
    rules: pd.DataFrame,
    purchased_products: Set[str],
    n_recommendations: int = 5
) -> List[str]:
    """
    Génère des recommandations basées sur les règles d'association.
    
    Args:
        rules (pd.DataFrame): Règles d'association
        purchased_products (Set[str]): Produits déjà achetés
        n_recommendations (int): Nombre de recommandations à générer
        
    Returns:
        List[str]: Liste des produits recommandés
    """
    recommendations = []
    
    # Filtrer les règles pertinentes
    for _, rule in rules.iterrows():
        antecedents = set(rule["antecedents"])
        consequents = set(rule["consequents"])
        
        # Si les antécédents sont dans les achats mais pas les conséquents
        if antecedents.issubset(purchased_products) and not consequents.issubset(purchased_products):
            for product in consequents:
                if product not in recommendations and product not in purchased_products:
                    recommendations.append(product)
                    if len(recommendations) >= n_recommendations:
                        return recommendations
    
    return recommendations

def get_popular_products_in_segment(
    data: pd.DataFrame,
    similar_customers: List[int],
    purchased_products: Set[str],
    n_recommendations: int = 5
) -> List[str]:
    """
    Trouve les produits populaires parmi les clients similaires.
    
    Args:
        data (pd.DataFrame): Données nettoyées
        similar_customers (List[int]): Liste des clients similaires
        purchased_products (Set[str]): Produits déjà achetés
        n_recommendations (int): Nombre de recommandations à générer
        
    Returns:
        List[str]: Liste des produits recommandés
    """
    # Obtenir les produits des clients similaires
    segment_purchases = data[data["CustomerID"].isin(similar_customers)]
    
    # Compter la fréquence des produits
    product_counts = segment_purchases["Description"].value_counts()
    
    # Filtrer les produits déjà achetés
    recommendations = [
        product for product in product_counts.index
        if product not in purchased_products
    ][:n_recommendations]
    
    return recommendations

def generate_recommendations(
    data: pd.DataFrame,
    rfm_df: pd.DataFrame,
    rules: pd.DataFrame,
    config: Dict[str, Any]
) -> pd.DataFrame:
    """
    Génère des recommandations personnalisées pour chaque client.
    
    Args:
        data (pd.DataFrame): Données nettoyées
        rfm_df (pd.DataFrame): Données RFM avec clusters
        rules (pd.DataFrame): Règles d'association
        config (Dict[str, Any]): Configuration
        
    Returns:
        pd.DataFrame: DataFrame avec les recommandations
    """
    logger.info("Début de la génération des recommandations")
    
    try:
        recommendations_dict = defaultdict(list)
        n_recommendations = config["recommendation"]["n_recommendations"]
        
        # Pour chaque client
        for customer_id in rfm_df["CustomerID"].unique():
            purchased_products = get_customer_purchases(data, customer_id)
            recommendations = []
            
            # Recommandations basées sur les règles
            if config["recommendation"]["use_association_rules"]:
                rule_recommendations = get_recommendations_from_rules(
                    rules, purchased_products, n_recommendations
                )
                recommendations.extend(rule_recommendations)
            
            # Recommandations basées sur la similarité RFM
            if config["recommendation"]["use_rfm_similarity"] and len(recommendations) < n_recommendations:
                similar_customers = get_similar_customers(rfm_df, customer_id)
                popular_recommendations = get_popular_products_in_segment(
                    data,
                    similar_customers,
                    purchased_products,
                    n_recommendations - len(recommendations)
                )
                recommendations.extend(popular_recommendations)
            
            # Limiter au nombre souhaité
            recommendations = recommendations[:n_recommendations]
            recommendations_dict[customer_id] = recommendations
        
        # Créer le DataFrame final
        recommendations_df = pd.DataFrame.from_dict(
            recommendations_dict,
            orient="index",
            columns=[f"Recommendation_{i+1}" for i in range(n_recommendations)]
        ).reset_index()
        recommendations_df.columns = ["CustomerID"] + [f"Recommendation_{i+1}" for i in range(n_recommendations)]
        
        # Sauvegarder
        save_dataframe(recommendations_df, config["paths"]["recommendations"])
        
        logger.info(f"Recommandations générées pour {len(recommendations_df)} clients")
        return recommendations_df
        
    except Exception as e:
        logger.error(f"Erreur lors de la génération des recommandations: {str(e)}")
        raise