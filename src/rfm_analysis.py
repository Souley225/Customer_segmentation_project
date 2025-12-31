"""
Module d'analyse RFM
Calcul des scores et segmentation des clients
"""
import pandas as pd
from datetime import timedelta
from src.utils import load_config

def calculate_rfm(df, snapshot_date=None):
    """Calcul des métriques RFM"""
    config = load_config()
    if snapshot_date is None:
        snapshot_date = df['InvoiceDate'].max() + timedelta(days=config['rfm']['snapshot_days'])
    
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'TotalPrice': 'sum'
    }).rename(columns={
        'InvoiceDate': 'Récence',
        'InvoiceNo': 'Fréquence', 
        'TotalPrice': 'Montant'
    })
    return rfm

def score_rfm(rfm):
    """Calcul des scores RFM (1-5)"""
    config = load_config()
    
    # Score Récence (inversé)
    rfm['R_score'] = pd.qcut(rfm['Récence'], config['rfm']['recency_quantiles'], 
                           labels=list(range(config['rfm']['recency_quantiles'], 0, -1)))
    
    # Scores Fréquence et Montant
    rfm['F_score'] = pd.qcut(rfm['Fréquence'].rank(method='first'), 
                           config['rfm']['frequency_quantiles'], 
                           labels=list(range(1, config['rfm']['frequency_quantiles'] + 1)))
    rfm['M_score'] = pd.qcut(rfm['Montant'], config['rfm']['monetary_quantiles'], 
                           labels=list(range(1, config['rfm']['monetary_quantiles'] + 1)))
    
    rfm['RFM_score'] = (rfm['R_score'].astype(str) + rfm['F_score'].astype(str) + 
                       rfm['M_score'].astype(str))
    return rfm

def map_rfm_to_segment(r_score, f_score, m_score):
    """Mapping des scores RFM vers segments"""
    if r_score >= 4 and f_score >= 4 and m_score >= 4:
        return 'Champions'
    elif r_score >= 2 and f_score >= 3 and m_score >= 3:
        return 'Clients Fidèles'
    elif r_score >= 3 and f_score >= 2 and m_score >= 3:
        return 'Potentiels Fidèles'
    elif r_score >= 4 and f_score <= 1:
        return 'Nouveaux Clients'
    elif r_score <= 1 and f_score >= 4 and m_score >= 4:
        return 'À Ne Pas Perdre'
    elif r_score <= 1 and f_score <= 2 and m_score <= 2:
        return 'Hibernants'
    else:
        return 'Autre'

def compute_segment_evolution(df):
    """Évolution des segments dans le temps"""
    quarters = pd.date_range(df['InvoiceDate'].min(), df['InvoiceDate'].max(), freq='Q')
    segments_dict = {}
    
    for q in quarters:
        rfm_q = calculate_rfm(df, q + timedelta(days=1))
        if not rfm_q.empty:
            rfm_q = score_rfm(rfm_q)
            rfm_q['Segment'] = rfm_q.apply(
                lambda row: map_rfm_to_segment(int(row['R_score']), int(row['F_score']), int(row['M_score'])), 
                axis=1
            )
            segments_dict[q.strftime('%Y-%m')] = rfm_q['Segment'].value_counts()
    
    return pd.DataFrame(segments_dict).T.fillna(0)