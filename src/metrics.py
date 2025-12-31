"""
Module de calcul des métriques
Calcul des métriques globales et par segment
"""
import pandas as pd
import numpy as np

def compute_global_metrics(df):
    """
    Calcul des métriques globales

    Returns:
        dict: CA, panier_moyen, nb_commandes, top_items
    """
    ca_total = df['TotalPrice'].sum()
    nb_commandes = df['InvoiceNo'].nunique()
    panier_moyen = ca_total / nb_commandes if nb_commandes > 0 else 0
    nb_clients = df['CustomerID'].nunique()

    # Top 5 items par CA
    top_items = (df.groupby('Description')['TotalPrice']
                 .sum()
                 .sort_values(ascending=False)
                 .head(5))

    return {
        'ca_total': ca_total,
        'panier_moyen': panier_moyen,
        'nb_commandes': nb_commandes,
        'nb_clients': nb_clients,
        'top_items': top_items
    }

def compute_segment_metrics(df, rfm, segment):
    """
    Calcul des métriques pour un segment spécifique

    Args:
        df: DataFrame des transactions
        rfm: DataFrame RFM avec colonne Segment
        segment: nom du segment

    Returns:
        dict: CA, panier_moyen, nb_commandes, top_items
    """
    # Récupérer les CustomerID du segment
    segment_customers = rfm[rfm['Segment'] == segment].index.tolist()

    # Filtrer les transactions du segment
    df_segment = df[df['CustomerID'].isin(segment_customers)]

    if len(df_segment) == 0:
        return {
            'ca_total': 0,
            'panier_moyen': 0,
            'nb_commandes': 0,
            'top_items': pd.Series(dtype=float)
        }

    ca_total = df_segment['TotalPrice'].sum()
    nb_commandes = df_segment['InvoiceNo'].nunique()
    panier_moyen = ca_total / nb_commandes if nb_commandes > 0 else 0

    # Top 5 items par CA
    top_items = (df_segment.groupby('Description')['TotalPrice']
                 .sum()
                 .sort_values(ascending=False)
                 .head(5))

    return {
        'ca_total': ca_total,
        'panier_moyen': panier_moyen,
        'nb_commandes': nb_commandes,
        'top_items': top_items
    }

def get_all_segments_metrics(df, rfm):
    """
    Calcul des métriques pour tous les segments

    Returns:
        DataFrame avec métriques par segment
    """
    segments = rfm['Segment'].unique()
    metrics_list = []
    ca_total_global = df['TotalPrice'].sum()

    for segment in segments:
        metrics = compute_segment_metrics(df, rfm, segment)
        nb_clients = len(rfm[rfm['Segment'] == segment])
        ca_segment = metrics['ca_total']
        
        metrics_list.append({
            'Segment': segment,
            'Clients': nb_clients,
            'Part Clients': nb_clients / len(rfm) * 100,
            'CA': ca_segment,
            'Part CA': ca_segment / ca_total_global * 100 if ca_total_global > 0 else 0,
            'Panier Moyen': metrics['panier_moyen'],
            'Commandes': metrics['nb_commandes'],
            'Valeur Client': ca_segment / nb_clients if nb_clients > 0 else 0
        })

    return pd.DataFrame(metrics_list).sort_values('CA', ascending=False)


def compute_business_insights(df, rfm):
    """
    Calcul des insights business pour les stakeholders
    
    Returns:
        dict: Indicateurs stratégiques
    """
    ca_total = df['TotalPrice'].sum()
    nb_clients_total = len(rfm)
    
    # Concentration du CA (règle 80/20)
    client_revenue = df.groupby('CustomerID')['TotalPrice'].sum().sort_values(ascending=False)
    cumsum = client_revenue.cumsum() / ca_total
    nb_clients_80_pct = (cumsum <= 0.80).sum()
    concentration_80_20 = nb_clients_80_pct / nb_clients_total * 100
    
    # Clients à risque (haute valeur, récence élevée)
    rfm_copy = rfm.copy()
    high_value_threshold = rfm_copy['Montant'].quantile(0.75)
    high_recency_threshold = rfm_copy['Récence'].quantile(0.75)
    clients_a_risque = rfm_copy[
        (rfm_copy['Montant'] >= high_value_threshold) & 
        (rfm_copy['Récence'] >= high_recency_threshold)
    ]
    nb_clients_risque = len(clients_a_risque)
    ca_risque = clients_a_risque['Montant'].sum()
    
    # Opportunités de croissance (fréquence faible, montant moyen)
    low_freq_threshold = rfm_copy['Fréquence'].quantile(0.25)
    medium_value = rfm_copy['Montant'].quantile(0.50)
    opportunites = rfm_copy[
        (rfm_copy['Fréquence'] <= low_freq_threshold) & 
        (rfm_copy['Montant'] >= medium_value)
    ]
    nb_opportunites = len(opportunites)
    
    # Taux de rétention estimé (clients actifs < 90 jours)
    clients_actifs = rfm_copy[rfm_copy['Récence'] <= 90]
    taux_retention = len(clients_actifs) / nb_clients_total * 100
    
    # Valeur client moyenne
    valeur_client_moyenne = ca_total / nb_clients_total
    
    # Top segment par CA
    segment_ca = rfm_copy.groupby('Segment')['Montant'].sum().sort_values(ascending=False)
    top_segment = segment_ca.index[0] if len(segment_ca) > 0 else "N/A"
    top_segment_pct = segment_ca.iloc[0] / ca_total * 100 if len(segment_ca) > 0 else 0
    
    return {
        'concentration_80_20': concentration_80_20,
        'nb_clients_80_pct': nb_clients_80_pct,
        'nb_clients_risque': nb_clients_risque,
        'ca_risque': ca_risque,
        'pct_ca_risque': ca_risque / ca_total * 100 if ca_total > 0 else 0,
        'nb_opportunites': nb_opportunites,
        'taux_retention': taux_retention,
        'valeur_client_moyenne': valeur_client_moyenne,
        'top_segment': top_segment,
        'top_segment_pct': top_segment_pct
    }


def get_segment_actions(segment):
    """
    Retourne les actions recommandées par segment
    """
    actions = {
        'Champions': {
            'priorite': 'Haute',
            'action': 'Fidélisation premium',
            'tactique': 'Programme VIP, accès exclusif, récompenses personnalisées'
        },
        'Clients Fidèles': {
            'priorite': 'Haute',
            'action': 'Upsell et cross-sell',
            'tactique': 'Recommandations personnalisées, offres bundle'
        },
        'Potentiels Fidèles': {
            'priorite': 'Moyenne',
            'action': 'Conversion en fidèles',
            'tactique': 'Programme de fidélité, communications régulières'
        },
        'Nouveaux Clients': {
            'priorite': 'Moyenne',
            'action': 'Onboarding optimisé',
            'tactique': 'Séquence bienvenue, guide produits, première offre'
        },
        'À Ne Pas Perdre': {
            'priorite': 'Critique',
            'action': 'Réactivation urgente',
            'tactique': 'Contact direct, offre exceptionnelle, enquête satisfaction'
        },
        'Hibernants': {
            'priorite': 'Basse',
            'action': 'Campagne de réactivation',
            'tactique': 'Email win-back, promotion agressive si ROI positif'
        },
        'Autre': {
            'priorite': 'Basse',
            'action': 'Analyse approfondie',
            'tactique': 'Segmentation plus fine, A/B testing'
        }
    }
    return actions.get(segment, actions['Autre'])
