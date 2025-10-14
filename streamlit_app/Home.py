"""
Page d'accueil de l'application Streamlit.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

from src.utils import load_config
from src.visualization import (
    plot_rfm_distribution,
    plot_segment_summary
)

# Charger la configuration
config = load_config()

# Configuration de la page
st.set_page_config(
    page_title=config["streamlit"]["page_title"],
    layout="wide"
)

def load_data():
    """Charge les données nécessaires."""
    rfm_data = pd.read_csv(config["paths"]["rfm_output"])
    clean_data = pd.read_csv(
        config["paths"]["processed_data"],
        parse_dates=["InvoiceDate"]
    )
    return clean_data, rfm_data

def calculate_kpis(data, rfm_data):
    """Calcule les KPIs principaux."""
    # Période d'analyse
    end_date = data["InvoiceDate"].max()
    start_date = end_date - timedelta(days=30)
    recent_data = data[data["InvoiceDate"] >= start_date]
    
    return {
        "ca_total": data["TotalPrice"].sum(),
        "ca_periode": recent_data["TotalPrice"].sum(),
        "nb_clients": len(data["CustomerID"].unique()),
        "nb_clients_actifs": len(recent_data["CustomerID"].unique()),
        "panier_moyen": data.groupby("InvoiceNo")["TotalPrice"].sum().mean(),
        "nb_segments": len(rfm_data["Segment"].unique())
    }

def main():
    """Fonction principale de la page d'accueil."""
    
    # Titre de la page
    st.title("Tableau de Bord des Insights Clients")
    
    try:
        # Charger les données
        data, rfm_data = load_data()
        
        # Calculer les KPIs
        kpis = calculate_kpis(data, rfm_data)
        
        # Afficher les KPIs
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Chiffre d'affaires total",
                f"{kpis['ca_total']:,.2f} {config['streamlit']['currency']}"
            )
            st.metric(
                "Nombre de clients",
                f"{kpis['nb_clients']:,}"
            )
            
        with col2:
            st.metric(
                "CA 30 derniers jours",
                f"{kpis['ca_periode']:,.2f} {config['streamlit']['currency']}"
            )
            st.metric(
                "Clients actifs (30j)",
                f"{kpis['nb_clients_actifs']:,}"
            )
            
        with col3:
            st.metric(
                "Panier moyen",
                f"{kpis['panier_moyen']:,.2f} {config['streamlit']['currency']}"
            )
            st.metric(
                "Nombre de segments",
                f"{kpis['nb_segments']}"
            )
        
        # Visualisations RFM
        st.header("Analyse RFM")
        
        tab1, tab2 = st.tabs(["Distribution des métriques", "Profils des segments"])
        
        with tab1:
            metric = st.selectbox(
                "Choisir une métrique",
                ["Recency", "Frequency", "Monetary"]
            )
            fig = plot_rfm_distribution(rfm_data, metric, config)
            st.plotly_chart(fig, use_container_width=True)
            
        with tab2:
            fig = plot_segment_summary(rfm_data, config)
            st.plotly_chart(fig, use_container_width=True)
        
        # Téléchargement des données
        st.sidebar.header("Exporter les données")
        
        if st.sidebar.button("Télécharger segmentation RFM"):
            rfm_data.to_csv("temp_rfm_export.csv", index=False)
            with open("temp_rfm_export.csv", "rb") as file:
                st.sidebar.download_button(
                    "Confirmer le téléchargement",
                    file,
                    "segmentation_rfm.csv",
                    "text/csv"
                )
        
    except Exception as e:
        st.error(f"Une erreur s'est produite: {str(e)}")
        st.error("Vérifiez que les fichiers de données existent et sont accessibles.")

if __name__ == "__main__":
    main()