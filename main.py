"""
Pipeline principal : nettoyage, segmentation RFM, analyse de panier et recommandations.
Compatible avec le fichier config/config.yaml fourni.
"""



import logging
from typing import Dict, Any
from pathlib import Path

from src.utils import load_config, setup_logger, save_dataframe
from src.data_preprocessing import clean_data, validate_data
from src.rfm_analysis import run_rfm_segmentation
from src.basket_analysis import run_association_rules
from src.recommendations import generate_recommendations


def create_directory_structure(config: Dict[str, Any]) -> None:
    """Crée les répertoires nécessaires à partir du fichier YAML."""
    directories = [
        config["paths"]["models_dir"],
        Path(config["paths"]["processed_data"]).parent,
        Path(config["paths"]["rfm_output"]).parent,
        Path(config["paths"]["association_rules"]).parent,
        Path(config["paths"]["recommendations"]).parent,
        config["paths"]["logs_dir"],
    ]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


def main():
    """Exécute le pipeline complet."""
    config = load_config()
    create_directory_structure(config)

    logger = setup_logger(log_path=f"{config['paths']['logs_dir']}/project.log")
    logger.info("===== DÉBUT DU PIPELINE =====")

    try:
        # Étape 1. Nettoyage des données
        logger.info("Étape 1 : Nettoyage des données")
        df_clean = clean_data(config)
        if not validate_data(df_clean):
            raise ValueError("La validation des données a échoué.")
        save_dataframe(df_clean, config["paths"]["processed_data"])
        logger.info(f"Données nettoyées sauvegardées dans {config['paths']['processed_data']}")

        # Étape 2. Segmentation RFM
        logger.info("Étape 2 : Segmentation RFM")
        rfm_df, rfm_model = run_rfm_segmentation(df_clean, config)
        save_dataframe(rfm_df, config["paths"]["rfm_output"])
        logger.info(f"Résultats RFM sauvegardés dans {config['paths']['rfm_output']}")

        # Étape 3. Analyse de panier
        logger.info("Étape 3 : Analyse de panier")
        rules_df, network = run_association_rules(df_clean, config)
        save_dataframe(rules_df, config["paths"]["association_rules"])
        logger.info(f"Règles d’association sauvegardées dans {config['paths']['association_rules']}")

        # Étape 4. Recommandations
        logger.info("Étape 4 : Génération des recommandations")
        recommendations_df = generate_recommendations(df_clean, rfm_df, rules_df, config)
        save_dataframe(recommendations_df, config["paths"]["recommendations"])
        logger.info(f"Recommandations sauvegardées dans {config['paths']['recommendations']}")

        logger.info("===== PIPELINE TERMINÉ AVEC SUCCÈS =====")

        return {
            "clean_data": df_clean,
            "rfm_data": rfm_df,
            "rules": rules_df,
            "recommendations": recommendations_df,
            "network": network,
        }

    except Exception as e:
        logger.exception(f"Erreur pendant l'exécution du pipeline : {e}")
        raise


if __name__ == "__main__":
    main()
