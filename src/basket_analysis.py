"""
Module d'analyse de panier (market basket analysis) pour identifier les associations de produits.
"""

import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
import networkx as nx
import logging
from typing import Dict, Any, Tuple, List
from src.utils import save_dataframe

logger = logging.getLogger(__name__)

def create_basket_matrix(data: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    """
    Crée une matrice transaction-produit pour l'analyse de panier.
    
    Args:
        data (pd.DataFrame): Données nettoyées
        config (Dict[str, Any]): Configuration
        
    Returns:
        pd.DataFrame: Matrice binaire transaction-produit
    """
    # Créer une table pivot
    basket_matrix = pd.crosstab(
        index=data[config["basket_analysis"]["invoice_col"]],
        columns=data[config["basket_analysis"]["product_col"]]
    )
    
    # Convertir en matrice binaire (1 si produit présent, 0 sinon)
    basket_matrix = (basket_matrix > 0).astype(int)
    
    return basket_matrix

def extract_rules(basket_matrix: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    """
    Extrait les règles d'association à partir de la matrice de paniers.
    
    Args:
        basket_matrix (pd.DataFrame): Matrice transaction-produit
        config (Dict[str, Any]): Configuration
        
    Returns:
        pd.DataFrame: Règles d'association
    """
    # Sélectionner l'algorithme
    if config["basket_analysis"]["algorithm"] == "apriori":
        frequent_itemsets = apriori(
            basket_matrix,
            min_support=config["basket_analysis"]["min_support"],
            use_colnames=True,
            max_len=config["basket_analysis"]["max_len"]
        )
    elif config["basket_analysis"]["algorithm"] == "fpgrowth":
        frequent_itemsets = fpgrowth(
            basket_matrix,
            min_support=config["basket_analysis"]["min_support"],
            use_colnames=True,
            max_len=config["basket_analysis"]["max_len"]
        )
    else:
        raise ValueError(f"Algorithme non supporté: {config['basket_analysis']['algorithm']}")
    
    # Générer les règles
    rules = association_rules(
        frequent_itemsets,
        metric="lift",
        min_threshold=config["basket_analysis"]["min_confidence"]
    )
    
    # Filtrer par lift minimum
    rules = rules[rules["lift"] >= config["basket_analysis"]["min_lift"]]
    
    return rules

def create_network_graph(rules: pd.DataFrame) -> nx.Graph:
    """
    Crée un graphe de réseau des associations de produits.
    
    Args:
        rules (pd.DataFrame): Règles d'association
        
    Returns:
        nx.Graph: Graphe de réseau
    """
    G = nx.Graph()
    
    for _, rule in rules.iterrows():
        # Ajouter les arêtes pour chaque paire antécédent-conséquent
        for antecedent in rule["antecedents"]:
            for consequent in rule["consequents"]:
                G.add_edge(
                    antecedent,
                    consequent,
                    weight=rule["lift"],
                    confidence=rule["confidence"]
                )
    
    return G

def format_rules_for_export(rules: pd.DataFrame) -> pd.DataFrame:
    """
    Formate les règles pour l'export en CSV.
    
    Args:
        rules (pd.DataFrame): Règles d'association brutes
        
    Returns:
        pd.DataFrame: Règles formatées
    """
    # Convertir les frozensets en listes pour le stockage
    rules_export = rules.copy()
    rules_export["antecedents"] = rules_export["antecedents"].apply(list)
    rules_export["consequents"] = rules_export["consequents"].apply(list)
    
    # Ajouter des colonnes formatées pour l'affichage
    rules_export["antecedents_str"] = rules_export["antecedents"].apply(lambda x: " + ".join(x))
    rules_export["consequents_str"] = rules_export["consequents"].apply(lambda x: " + ".join(x))
    
    return rules_export

def run_association_rules(data: pd.DataFrame, config: Dict[str, Any]) -> Tuple[pd.DataFrame, nx.Graph]:
    """
    Exécute l'analyse complète des règles d'association.
    
    Args:
        data (pd.DataFrame): Données nettoyées
        config (Dict[str, Any]): Configuration
        
    Returns:
        Tuple[pd.DataFrame, nx.Graph]: Règles d'association et graphe de réseau
    """
    logger.info("Début de l'analyse des règles d'association")
    
    try:
        # Créer la matrice de paniers
        basket_matrix = create_basket_matrix(data, config)
        logger.info(f"Matrice de paniers créée: {basket_matrix.shape[0]} transactions, {basket_matrix.shape[1]} produits")
        
        # Extraire les règles
        rules = extract_rules(basket_matrix, config)
        logger.info(f"{len(rules)} règles d'association trouvées")
        
        # Créer le graphe de réseau
        network = create_network_graph(rules)
        logger.info(f"Graphe créé avec {network.number_of_nodes()} nœuds et {network.number_of_edges()} arêtes")
        
        # Formater et sauvegarder les règles
        rules_export = format_rules_for_export(rules)
        save_dataframe(rules_export, config["paths"]["association_rules"])
        
        logger.info("Analyse des règles d'association terminée avec succès")
        return rules, network
        
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse des règles d'association: {str(e)}")
        raise