"""
Page d'analyse des règles d'association (market basket analysis).
"""

import streamlit as st
import pandas as pd
import networkx as nx
from src.utils import load_config
from src.visualization import plot_association_network

# Configuration
config = load_config()

st.set_page_config(
    page_title=f"{config['streamlit']['page_title']} - Analyse de panier",
    layout="wide"
)

def load_data():
    """Charge les règles d'association."""
    rules = pd.read_csv(config["paths"]["association_rules"])
    
    # Convertir les chaînes en listes
    rules["antecedents"] = rules["antecedents_str"].str.split(" + ")
    rules["consequents"] = rules["consequents_str"].str.split(" + ")
    
    return rules

def filter_rules(rules, min_support, min_confidence, min_lift):
    """Filtre les règles selon les seuils."""
    return rules[
        (rules["support"] >= min_support) &
        (rules["confidence"] >= min_confidence) &
        (rules["lift"] >= min_lift)
    ]

def display_rule_details(rule):
    """Affiche les détails d'une règle."""
    st.write("**Si un client achète:**")
    for item in rule["antecedents"]:
        st.write(f"- {item}")
        
    st.write("**Alors il pourrait aussi acheter:**")
    for item in rule["consequents"]:
        st.write(f"- {item}")
        
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Support", f"{rule['support']:.3f}")
    with col2:
        st.metric("Confiance", f"{rule['confidence']:.3f}")
    with col3:
        st.metric("Lift", f"{rule['lift']:.3f}")

def main():
    """Fonction principale de la page d'analyse de panier."""
    st.title("Analyse des Associations de Produits")
    
    try:
        # Charger les données
        rules = load_data()
        
        # Filtres
        st.sidebar.header("Filtres")
        
        min_support = st.sidebar.slider(
            "Support minimum",
            min_value=0.0,
            max_value=1.0,
            value=config["basket_analysis"]["min_support"],
            step=0.01
        )
        
        min_confidence = st.sidebar.slider(
            "Confiance minimum",
            min_value=0.0,
            max_value=1.0,
            value=config["basket_analysis"]["min_confidence"],
            step=0.01
        )
        
        min_lift = st.sidebar.slider(
            "Lift minimum",
            min_value=1.0,
            max_value=10.0,
            value=config["basket_analysis"]["min_lift"],
            step=0.1
        )
        
        # Filtrer les règles
        filtered_rules = filter_rules(rules, min_support, min_confidence, min_lift)
        
        # Afficher les statistiques
        st.header("Aperçu des règles")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Nombre de règles", len(filtered_rules))
        with col2:
            st.metric("Lift moyen", f"{filtered_rules['lift'].mean():.2f}")
        with col3:
            st.metric(
                "Confiance moyenne",
                f"{filtered_rules['confidence'].mean():.2%}"
            )
        
        # Visualisation du réseau
        st.header("Réseau d'associations")
        
        max_nodes = st.slider(
            "Nombre maximum de nœuds",
            min_value=5,
            max_value=50,
            value=20
        )
        
        network = nx.Graph()
        for _, rule in filtered_rules.iterrows():
            for a in rule["antecedents"]:
                for c in rule["consequents"]:
                    network.add_edge(a, c, weight=rule["lift"])
        
        fig = plot_association_network(
            network,
            min_edge_weight=min_lift,
            max_nodes=max_nodes
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Liste des meilleures règles
        st.header("Meilleures règles d'association")
        
        sort_by = st.selectbox(
            "Trier par",
            ["lift", "confidence", "support"]
        )
        
        top_rules = filtered_rules.nlargest(10, sort_by)
        for idx, rule in top_rules.iterrows():
            with st.expander(
                f"Règle {idx+1} (Lift: {rule['lift']:.2f})"
            ):
                display_rule_details(rule)
        
        # Export des règles
        st.sidebar.header("Exporter les données")
        
        if st.sidebar.button("Télécharger les règles filtrées"):
            filtered_rules.to_csv("temp_rules_export.csv", index=False)
            with open("temp_rules_export.csv", "rb") as file:
                st.sidebar.download_button(
                    "Confirmer le téléchargement",
                    file,
                    "regles_association.csv",
                    "text/csv"
                )
        
    except Exception as e:
        st.error(f"Une erreur s'est produite: {str(e)}")
        st.error("Vérifiez que les fichiers de données existent et sont accessibles.")

if __name__ == "__main__":
    main()