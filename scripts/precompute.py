"""
Script de pré-calcul des données
Exécuter avant chaque déploiement pour des temps de chargement optimaux
"""
import os
import sys
import pickle

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_preprocessing import load_and_clean_data
from src.rfm_analysis import calculate_rfm, score_rfm, map_rfm_to_segment
from src.basket_analysis import perform_basket_analysis

def main():
    print("=" * 50)
    print("PRECOMPUTE - Pipeline de calcul des donnees")
    print("=" * 50)
    
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed')
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Chargement et nettoyage des données
    print("\n[1/4] Chargement des donnees brutes...")
    df = load_and_clean_data()
    print(f"      {len(df):,} transactions chargees")
    
    # 2. Calcul RFM
    print("[2/4] Calcul des scores RFM...")
    rfm = calculate_rfm(df)
    rfm_scored = score_rfm(rfm)
    rfm_scored['Segment'] = rfm_scored.apply(
        lambda row: map_rfm_to_segment(int(row['R_score']), int(row['F_score']), int(row['M_score'])),
        axis=1
    )
    print(f"      {len(rfm_scored):,} clients segmentes")
    
    # 3. Analyse de panier
    print("[3/4] Analyse de panier (regles d'association)...")
    rules = perform_basket_analysis(df)
    print(f"      {len(rules):,} regles generees")
    
    # 4. Sauvegarde
    print("[4/4] Sauvegarde des fichiers...")
    
    # Transactions nettoyées
    df.to_csv(os.path.join(output_dir, 'transactions.csv'), index=False)
    print(f"      -> transactions.csv")
    
    # RFM avec segments
    rfm_scored.to_csv(os.path.join(output_dir, 'rfm_segments.csv'))
    print(f"      -> rfm_segments.csv")
    
    # Règles d'association (pickle car contient des frozensets)
    with open(os.path.join(output_dir, 'association_rules.pkl'), 'wb') as f:
        pickle.dump(rules, f)
    print(f"      -> association_rules.pkl")
    
    print("\n" + "=" * 50)
    print("TERMINE - Fichiers prets pour deploiement")
    print("=" * 50)
    print(f"\nRepertoire: {output_dir}")
    print("\nProchaine etape: git add data/processed/ && git push")

if __name__ == "__main__":
    main()
