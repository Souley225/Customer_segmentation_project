"""
Module d'analyse RFM (Recency, Frequency, Monetary) et segmentation client.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from datetime import datetime
import joblib
import logging
from typing import Dict, Any, Tuple
from .utils import save_dataframe

logger = logging.getLogger(__name__)

def calculate_rfm_metrics(data: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    """
    Calcule les métriques RFM pour chaque client.
    
    Args:
        data (pd.DataFrame): Données nettoyées
        config (Dict[str, Any]): Configuration du projet
        
    Returns:
        pd.DataFrame: DataFrame avec métriques RFM
    """
    # Extraire les paramètres de configuration
    reference_date = datetime.strptime(config["rfm"]["reference_date"], "%Y-%m-%d")
    
    # Calculer les métriques RFM par client
    rfm = data.groupby("CustomerID").agg({
        config["rfm"]["recency_col"]: lambda x: (reference_date - x.max()).days,
        config["rfm"]["frequency_col"]: "count",
        config["rfm"]["monetary_col"]: "sum"
    }).reset_index()
    
    # Renommer les colonnes
    rfm.columns = ["CustomerID", "Recency", "Frequency", "Monetary"]
    
    return rfm

def normalize_rfm(rfm_df: pd.DataFrame, config: Dict[str, Any]) -> Tuple[pd.DataFrame, StandardScaler]:
    """
    Normalise les métriques RFM si spécifié dans la configuration.
    
    Args:
        rfm_df (pd.DataFrame): DataFrame RFM
        config (Dict[str, Any]): Configuration
        
    Returns:
        Tuple[pd.DataFrame, StandardScaler]: DataFrame normalisé et scaler
    """
    if not config["rfm"]["normalize"]:
        return rfm_df, None
        
    features = ["Recency", "Frequency", "Monetary"]
    scaler = StandardScaler()
    
    # Transformer Recency en valeur positive (plus grand = plus récent)
    rfm_df["Recency"] = rfm_df["Recency"].max() - rfm_df["Recency"]
    
    # Normaliser les features
    rfm_scaled = scaler.fit_transform(rfm_df[features])
    rfm_normalized = pd.DataFrame(rfm_scaled, columns=features)
    rfm_normalized["CustomerID"] = rfm_df["CustomerID"]
    
    return rfm_normalized, scaler

def perform_clustering(rfm_normalized: pd.DataFrame, config: Dict[str, Any]) -> Tuple[pd.DataFrame, object]:
    """
    Applique l'algorithme de clustering sur les données RFM.
    
    Args:
        rfm_normalized (pd.DataFrame): Données RFM normalisées
        config (Dict[str, Any]): Configuration
        
    Returns:
        Tuple[pd.DataFrame, object]: DataFrame avec clusters et modèle
    """
    features = ["Recency", "Frequency", "Monetary"]
    
    if config["rfm"]["clustering_method"] == "kmeans":
        model = KMeans(
            n_clusters=config["rfm"]["n_clusters"],
            random_state=config["rfm"]["random_state"]
        )
    else:
        raise ValueError(f"Méthode de clustering non supportée: {config['rfm']['clustering_method']}")
    
    # Appliquer le clustering
    clusters = model.fit_predict(rfm_normalized[features])
    rfm_normalized["Cluster"] = clusters
    
    return rfm_normalized, model

def label_segments(rfm_with_clusters: pd.DataFrame) -> pd.DataFrame:
    """
    Attribue des labels aux segments selon leurs caractéristiques RFM.
    
    Args:
        rfm_with_clusters (pd.DataFrame): DataFrame RFM avec clusters
        
    Returns:
        pd.DataFrame: DataFrame avec labels de segments
    """
    # Calculer les moyennes par cluster
    cluster_means = rfm_with_clusters.groupby("Cluster")[["Recency", "Frequency", "Monetary"]].mean()
    
    # Créer un mapping des labels
    labels = {}
    for cluster in cluster_means.index:
        means = cluster_means.loc[cluster]
        
        if means["Monetary"] > cluster_means["Monetary"].median():
            if means["Recency"] > cluster_means["Recency"].median():
                labels[cluster] = "Champions"
            else:
                labels[cluster] = "Clients fidèles"
        else:
            if means["Recency"] > cluster_means["Recency"].median():
                labels[cluster] = "Clients potentiels"
            else:
                labels[cluster] = "Clients à risque"
    
    rfm_with_clusters["Segment"] = rfm_with_clusters["Cluster"].map(labels)
    return rfm_with_clusters

def run_rfm_segmentation(data: pd.DataFrame, config: Dict[str, Any]) -> Tuple[pd.DataFrame, object]:
    """
    Exécute la segmentation RFM complète.
    
    Args:
        data (pd.DataFrame): Données nettoyées
        config (Dict[str, Any]): Configuration
        
    Returns:
        Tuple[pd.DataFrame, object]: DataFrame segmenté et modèle
    """
    logger.info("Début de la segmentation RFM")
    
    try:
        # Calculer métriques RFM
        rfm_df = calculate_rfm_metrics(data, config)
        logger.info(f"Métriques RFM calculées pour {len(rfm_df)} clients")
        
        # Normaliser
        rfm_normalized, scaler = normalize_rfm(rfm_df, config)
        
        # Clustering
        rfm_clustered, model = perform_clustering(rfm_normalized, config)
        
        # Labels
        final_rfm = label_segments(rfm_clustered)
        
        # Sauvegarder
        save_dataframe(final_rfm, config["paths"]["rfm_output"])
        joblib.dump(model, f"{config['paths']['models_dir']}/rfm_model.pkl")
        if scaler:
            joblib.dump(scaler, f"{config['paths']['models_dir']}/rfm_scaler.pkl")
        
        logger.info("Segmentation RFM terminée avec succès")
        return final_rfm, model
        
    except Exception as e:
        logger.error(f"Erreur lors de la segmentation RFM: {str(e)}")
        raise