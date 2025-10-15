"""
Module de recommandations
Stratégies multiples de recommandation
"""
import pandas as pd
from src.data_preprocessing import load_config

def get_customer_recommendations(df, rfm, rules, customer_id):
    """Génération des recommandations pour un client"""
    config = load_config()
    recommendations = {}
    
    history = df[df['CustomerID'] == customer_id]['Description'].unique()
    
    # 1. Règles d'association
    assoc_recs = set()
    for _, rule in rules.iterrows():
        if set(rule['antecedents']).issubset(history):
            assoc_recs.update(rule['consequents'])
    assoc_recs -= set(history)
    recommendations['Association'] = list(assoc_recs)[:config['recommendations']['top_n_rules']]
    
    # 2. Segment
    segment = rfm.loc[customer_id, 'Segment']
    segment_customers = rfm[rfm['Segment'] == segment].index
    segment_sales = (df[df['CustomerID'].isin(segment_customers)]
                    .groupby('Description')['TotalPrice'].sum()
                    .sort_values(ascending=False))
    segment_recs = set(segment_sales.head(config['recommendations']['top_n_segment']).index)
    segment_recs -= set(history)
    recommendations['Segment'] = list(segment_recs)
    
    return recommendations