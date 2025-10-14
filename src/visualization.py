"""
Module de visualisation pour la création de graphiques interactifs avec Plotly.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

def plot_rfm_distribution(df: pd.DataFrame, metric: str, config: Dict[str, Any]) -> go.Figure:
    """
    Crée un histogramme de distribution pour une métrique RFM.
    
    Args:
        df (pd.DataFrame): Données RFM
        metric (str): Métrique à visualiser ('Recency', 'Frequency', 'Monetary')
        config (Dict[str, Any]): Configuration
        
    Returns:
        go.Figure: Figure Plotly
    """
    fig = px.histogram(
        df,
        x=metric,
        color="Segment",
        nbins=30,
        title=f"Distribution de {metric} par segment",
        labels={metric: f"{metric} (normalisé)" if config["rfm"]["normalize"] else metric},
        color_discrete_sequence=px.colors.qualitative[config["visualization"]["palette"]]
    )
    
    fig.update_layout(
        template=config["visualization"]["theme"],
        showlegend=True,
        width=config["visualization"]["figsize"][0] * 100,
        height=config["visualization"]["figsize"][1] * 100
    )
    
    return fig

def plot_segment_summary(df: pd.DataFrame, config: Dict[str, Any]) -> go.Figure:
    """
    Crée un résumé visuel des segments RFM.
    
    Args:
        df (pd.DataFrame): Données RFM
        config (Dict[str, Any]): Configuration
        
    Returns:
        go.Figure: Figure Plotly
    """
    # Calculer les moyennes par segment
    segment_means = df.groupby("Segment")[["Recency", "Frequency", "Monetary"]].mean()
    
    # Créer le radar chart
    fig = go.Figure()
    
    for segment in segment_means.index:
        fig.add_trace(go.Scatterpolar(
            r=segment_means.loc[segment],
            theta=["Récence", "Fréquence", "Monétaire"],
            name=segment,
            fill="toself"
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1] if config["rfm"]["normalize"] else None
            )
        ),
        showlegend=True,
        title="Profils des segments RFM",
        template=config["visualization"]["theme"],
        width=config["visualization"]["figsize"][0] * 100,
        height=config["visualization"]["figsize"][1] * 100
    )
    
    return fig

def plot_association_network(
    network: nx.Graph,
    min_edge_weight: float = 1.5,
    max_nodes: int = 20
) -> go.Figure:
    """
    Crée une visualisation réseau des règles d'association.
    
    Args:
        network (nx.Graph): Graphe de réseau
        min_edge_weight (float): Poids minimum des arêtes à afficher
        max_nodes (int): Nombre maximum de nœuds à afficher
        
    Returns:
        go.Figure: Figure Plotly
    """
    # Filtrer les arêtes par poids
    filtered_edges = [(u, v) for u, v, d in network.edges(data=True) if d["weight"] >= min_edge_weight]
    
    # Créer un sous-graphe filtré
    sub_network = network.edge_subgraph(filtered_edges)
    
    # Limiter le nombre de nœuds
    if len(sub_network) > max_nodes:
        # Garder les nœuds avec le plus de connexions
        degrees = dict(sub_network.degree())
        top_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:max_nodes]
        sub_network = sub_network.subgraph([node for node, _ in top_nodes])
    
    # Calculer la disposition
    pos = nx.spring_layout(sub_network)
    
    # Créer le graphique
    edge_x = []
    edge_y = []
    edge_weights = []
    
    for edge in sub_network.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_weights.append(edge[2]["weight"])
    
    # Tracer les arêtes
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=1, color="#888"),
        hoverinfo="none",
        mode="lines"
    )
    
    # Tracer les nœuds
    node_x = []
    node_y = []
    node_text = []
    
    for node in sub_network.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(str(node))
    
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        hoverinfo="text",
        text=node_text,
        textposition="top center",
        marker=dict(
            size=10,
            line_width=2
        )
    )
    
    # Créer la figure finale
    fig = go.Figure(data=[edge_trace, node_trace],
        layout=go.Layout(
            title="Réseau des associations de produits",
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
    )
    
    return fig

def plot_customer_history(
    data: pd.DataFrame,
    customer_id: int,
    config: Dict[str, Any]
) -> go.Figure:
    """
    Crée un graphique de l'historique d'achat d'un client.
    
    Args:
        data (pd.DataFrame): Données nettoyées
        customer_id (int): ID du client
        config (Dict[str, Any]): Configuration
        
    Returns:
        go.Figure: Figure Plotly
    """
    # Filtrer les données du client
    customer_data = data[data["CustomerID"] == customer_id].copy()
    customer_data = customer_data.sort_values("InvoiceDate")
    
    # Créer le graphique
    fig = go.Figure()
    
    # Ajouter la ligne des achats cumulés
    cumulative_spending = customer_data["TotalPrice"].cumsum()
    
    fig.add_trace(go.Scatter(
        x=customer_data["InvoiceDate"],
        y=cumulative_spending,
        mode="lines+markers",
        name="Achats cumulés",
        line=dict(color=config["visualization"]["custom_colors"]["primary"])
    ))
    
    # Mettre à jour le layout
    currency = config["streamlit"]["currency"]
    fig.update_layout(
        title=f"Historique d'achat du client {customer_id}",
        xaxis_title="Date",
        yaxis_title=f"Montant cumulé ({currency})",
        template=config["visualization"]["theme"],
        width=config["visualization"]["figsize"][0] * 100,
        height=config["visualization"]["figsize"][1] * 100
    )
    
    return fig