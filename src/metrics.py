"""
Module de calcul des métriques
Calcul des métriques globales et par segment
"""
import pandas as pd

def compute_global_metrics(df):
    """
    Calcul des métriques globales

    Returns:
        dict: CA, panier_moyen, nb_commandes, top_items
    """
    ca_total = df['TotalPrice'].sum()
    nb_commandes = df['InvoiceNo'].nunique()
    panier_moyen = ca_total / nb_commandes if nb_commandes > 0 else 0

    # Top 5 items par CA
    top_items = (df.groupby('Description')['TotalPrice']
                 .sum()
                 .sort_values(ascending=False)
                 .head(5))

    return {
        'ca_total': ca_total,
        'panier_moyen': panier_moyen,
        'nb_commandes': nb_commandes,
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

    for segment in segments:
        metrics = compute_segment_metrics(df, rfm, segment)
        metrics_list.append({
            'Segment': segment,
            'CA': metrics['ca_total'],
            'Panier Moyen': metrics['panier_moyen'],
            'Nb Commandes': metrics['nb_commandes'],
            'Nb Clients': len(rfm[rfm['Segment'] == segment])
        })

    return pd.DataFrame(metrics_list).sort_values('CA', ascending=False)
