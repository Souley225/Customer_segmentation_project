"""
Script principal pour l'exécution du pipeline complet d'analyse client.
"""

import logging
from typing import Dict, Any
from pathlib import Path

from src.utils import load_config, setup_logger
from src.data_preprocessing import clean_data, validate_data
from src.rfm_analysis import run_rfm_segmentation
from src.basket_analysis import run_association_rules
from src.recommendations import generate_recommendations

def create_directory_structure(config: Dict[str, Any]) -> None:
    """
    Crée la structure des répertoires nécessaires.
    """
    directories = [
        config["paths"]["models_dir"],
        Path(config["paths"]["processed_data"]).parent,
        Path(config["paths"]["rfm_output"]).parent,
        Path(config["paths"]["association_rules"]).parent,
        Path(config["paths"]["recommendations"]).parent,
        Path(config["paths"]["logs_dir"])
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def main():
    """
    Fonction principale exécutant le pipeline complet.
    """
    # Charger la configuration
    config = load_config()
    
    # Créer la structure des répertoires
    create_directory_structure(config)
    
    # Configurer le logger
    logger = setup_logger(log_path=f"{config['paths']['logs_dir']}/project.log")
    logger.info("Début de l'exécution du pipeline")
    
    try:
        # 1. Nettoyage des données
        logger.info("Étape 1: Nettoyage des données")
        df_clean = clean_data(config)
        
        if not validate_data(df_clean):
            raise ValueError("La validation des données a échoué")
        
        # 2. Segmentation RFM
        logger.info("Étape 2: Segmentation RFM")
        rfm_df, rfm_model = run_rfm_segmentation(df_clean, config)
        
        # 3. Analyse de panier
        logger.info("Étape 3: Analyse de panier")
        rules_df, network = run_association_rules(df_clean, config)
        
        # 4. Génération des recommandations
        logger.info("Étape 4: Génération des recommandations")
        recommendations_df = generate_recommendations(
            df_clean,
            rfm_df,
            rules_df,
            config
        )
        
        logger.info("Pipeline exécuté avec succès")
        return {
            "clean_data": df_clean,
            "rfm_data": rfm_df,
            "rules": rules_df,
            "recommendations": recommendations_df,
            "network": network
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution du pipeline: {str(e)}")
        raise

if __name__ == "__main__":
    main()