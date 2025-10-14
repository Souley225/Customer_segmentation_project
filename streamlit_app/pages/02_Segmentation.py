"""
Page d'analyse détaillée des segments RFM.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from src.utils import load_config
from src.visualization import plot_segment_summary

# Configuration
config = load_config()

st.set_page_config(
    page_title=f"{config['streamlit']['page_title']} - Segmentation",
    layout="wide"
)

def load_data():
    """Charge les données RFM."""
    return pd.read_csv(config["paths"]["rfm_output"])

def plot_segment_metrics(data, segment):
    """Crée des visualisations pour un segment spécifique."""
    segment_data = data[data["Segment"] == segment]
    
    # Distribution des métriques
    figs = {}
    for metric in ["Recency", "Frequency", "Monetary"]:
        fig = px.histogram(
            segment_data,
            x=metric,
            title=f"Distribution de {metric} - {segment}",
            template=config["visualization"]["theme"]
        )
        figs[metric] = fig
    
    return figs

def calculate_segment_stats(data, segment):
    """Calcule les statistiques descriptives pour un segment."""
    segment_data = data[data["Segment"] == segment]
    
    stats = {
        "Taille du segment": len(segment_data),
        "% du total": len(segment_data) / len(data) * 100,
        "Moyenne Recency": segment_data["Recency"].mean(),
        "Moyenne Frequency": segment_data["Frequency"].mean(),
        "Moyenne Monetary": segment_data["Monetary"].mean(),
    }
    
    return stats

def main():
    """Fonction principale de la page de segmentation."""
    st.title("Analyse des Segments Clients")
    
    try:
        # Charger les données
        data = load_data()
        
        # Sélecteur de segment
        segments = sorted(data["Segment"].unique())
        selected_segment = st.selectbox(
            "Sélectionner un segment à analyser",
            segments
        )
        
        # Afficher les statistiques du segment
        st.header(f"Statistiques du segment : {selected_segment}")
        stats = calculate_segment_stats(data, selected_segment)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Nombre de clients",
                f"{stats['Taille du segment']:,}"
            )
            st.metric(
                "Part du total",
                f"{stats['% du total']:.1f}%"
            )
            
        with col2:
            st.metric(
                "Récence moyenne (jours)",
                f"{stats['Moyenne Recency']:.1f}"
            )
            st.metric(
                "Fréquence moyenne",
                f"{stats['Moyenne Frequency']:.1f}"
            )
            
        with col3:
            st.metric(
                "Panier moyen",
                f"{stats['Moyenne Monetary']:.2f} {config['streamlit']['currency']}"
            )
        
        # Visualisations
        st.header("Analyse des métriques")
        
        # Distributions des métriques
        figs = plot_segment_metrics(data, selected_segment)
        
        tab1, tab2, tab3 = st.tabs(["Récence", "Fréquence", "Monétaire"])
        
        with tab1:
            st.plotly_chart(figs["Recency"], use_container_width=True)
            
        with tab2:
            st.plotly_chart(figs["Frequency"], use_container_width=True)
            
        with tab3:
            st.plotly_chart(figs["Monetary"], use_container_width=True)
        
        # Comparaison avec autres segments
        st.header("Comparaison avec les autres segments")
        fig = plot_segment_summary(data, config)
        st.plotly_chart(fig, use_container_width=True)
        
        # Export des données du segment
        st.sidebar.header("Exporter les données")
        
        if st.sidebar.button(f"Télécharger données {selected_segment}"):
            segment_data = data[data["Segment"] == selected_segment]
            segment_data.to_csv("temp_segment_export.csv", index=False)
            with open("temp_segment_export.csv", "rb") as file:
                st.sidebar.download_button(
                    "Confirmer le téléchargement",
                    file,
                    f"segment_{selected_segment.lower()}.csv",
                    "text/csv"
                )
        
    except Exception as e:
        st.error(f"Une erreur s'est produite: {str(e)}")
        st.error("Vérifiez que les fichiers de données existent et sont accessibles.")

if __name__ == "__main__":
    main()