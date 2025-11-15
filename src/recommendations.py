"""
Module de recommandations
Stratégies multiples de recommandation
"""
import pandas as pd
from src.utils import load_config

def get_customer_recommendations(df, rfm, rules, customer_id):
    """
    Génération des recommandations pour un client avec lift

    Returns:
        dict: {
            'history': liste des achats précédents,
            'recommendations': liste de tuples (produit, lift, source)
        }
    """
    config = load_config()

    history = df[df['CustomerID'] == customer_id]['Description'].unique()
    recommendations_with_lift = []

    # 1. Règles d'association avec lift
    if not rules.empty:
        for _, rule in rules.iterrows():
            if set(rule['antecedents']).issubset(history):
                for cons in rule['consequents']:
                    if cons not in history:
                        recommendations_with_lift.append({
                            'produit': cons,
                            'lift': round(rule['lift'], 2),
                            'confidence': round(rule['confidence'], 2),
                            'source': 'Association'
                        })

    # 2. Recommandations par segment (sans lift car basé sur popularité)
    segment = rfm.loc[customer_id, 'Segment']
    segment_customers = rfm[rfm['Segment'] == segment].index
    segment_sales = (df[df['CustomerID'].isin(segment_customers)]
                    .groupby('Description')['TotalPrice'].sum()
                    .sort_values(ascending=False))

    for product in segment_sales.head(config['recommendations']['top_n_segment']).index:
        if product not in history:
            # Vérifier si déjà dans les recommandations
            if not any(r['produit'] == product for r in recommendations_with_lift):
                recommendations_with_lift.append({
                    'produit': product,
                    'lift': None,  # Pas de lift pour recommandations segment
                    'confidence': None,
                    'source': 'Segment'
                })

    # Trier par lift (les None à la fin)
    recommendations_with_lift.sort(
        key=lambda x: (x['lift'] is None, -x['lift'] if x['lift'] else 0),
        reverse=False
    )

    return {
        'history': list(history),
        'recommendations': recommendations_with_lift[:10]  # Top 10
    }