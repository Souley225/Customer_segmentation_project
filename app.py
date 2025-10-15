"""
Application Streamlit principale pour le tableau de bord de segmentation client
Déploiement sur Render
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_preprocessing import load_and_clean_data
from src.rfm_analysis import calculate_rfm, score_rfm, map_rfm_to_segment, compute_segment_evolution
from src.basket_analysis import perform_basket_analysis
from src.recommendations import get_customer_recommendations
from src.visualization import create_kpi_metrics, create_rfm_pie, create_segment_profiles, \
                              create_monetary_box, create_evolution_area, create_rules_table, \
                              create_support_confidence_scatter, create_association_graph
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(
    page_title="Tableau de Bord Segmentation Client",
    page_icon="📊",
    layout="wide"
)

st.title("Tableau de Bord Segmentation Client")

# Chargement des données
@st.cache_data
def load_app_data():
    """Chargement et préparation des données pour l'application"""
    df = load_and_clean_data()
    rfm = calculate_rfm(df)
    rfm_scored = score_rfm(rfm)
    rfm_scored['Segment'] = rfm_scored.apply(
        lambda row: map_rfm_to_segment(int(row['R_score']), int(row['F_score']), int(row['M_score'])), 
        axis=1
    )
    rules = perform_basket_analysis(df)
    evol_df = compute_segment_evolution(df)
    return df, rfm_scored, rules, evol_df

df, rfm, rules, evol_df = load_app_data()

# Interface avec onglets
tabs = st.tabs(['Vue Globale', 'Analyse des Segments', 'Analyse de Panier', 'Vue Client'])

with tabs[0]:
    create_kpi_metrics(df, rfm)
    create_rfm_pie(rfm)
    create_segment_profiles(rfm)

with tabs[1]:
    create_segment_profiles(rfm)
    create_monetary_box(rfm)
    create_evolution_area(evol_df)

with tabs[2]:
    create_rules_table(rules)
    create_support_confidence_scatter(rules)
    create_association_graph(rules)

with tabs[3]:
    customer_ids = sorted(rfm.index)
    customer_id = st.selectbox('Sélectionnez Client ID', customer_ids)
    
    if customer_id:
        recommendations = get_customer_recommendations(df, rfm, rules, customer_id)
        
        st.subheader('Profil RFM')
        profile = rfm.loc[customer_id][['Recency', 'Frequency', 'Monetary', 'Segment']]
        st.write(profile)
        
        st.subheader('Historique d\'Achat')
        history = df[df['CustomerID'] == customer_id][['InvoiceDate', 'Description', 'Quantity', 'TotalPrice']]
        st.dataframe(history.head(10))
        
        st.subheader('Recommandations Personnalisées')
        for rec_type, recs in recommendations.items():
            if recs:
                st.write(f"**{rec_type}:** {', '.join(recs[:5])}")
            else:
                st.write(f"**{rec_type}:** Aucune recommandation")