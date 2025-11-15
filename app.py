"""
Application Streamlit pour le tableau de bord de segmentation client
Déploiement sur Render
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_preprocessing import load_and_clean_data
from src.rfm_analysis import calculate_rfm, score_rfm, map_rfm_to_segment
from src.basket_analysis import perform_basket_analysis
from src.recommendations import get_customer_recommendations
from src.metrics import compute_global_metrics, compute_segment_metrics, get_all_segments_metrics

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
    return df, rfm_scored, rules

df, rfm, rules = load_app_data()

# Interface avec onglets
tabs = st.tabs(['Vue Globale des Segments', 'Vue par Segment', 'Recommandations Produit'])

# ========== ONGLET 1: VUE GLOBALE DES SEGMENTS ==========
with tabs[0]:
    st.header("Vue Globale sur les Segments")

    # Métriques globales
    global_metrics = compute_global_metrics(df)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("CA Total", f"£{global_metrics['ca_total']:,.2f}")
    with col2:
        st.metric("Panier Moyen", f"£{global_metrics['panier_moyen']:,.2f}")
    with col3:
        st.metric("Nombre Total de Commandes", f"{global_metrics['nb_commandes']:,}")

    # Top 5 items achetés
    st.subheader("Top 5 Items Achetés (par CA)")
    top_items_df = global_metrics['top_items'].reset_index()
    top_items_df.columns = ['Produit', 'CA Total']
    top_items_df['CA Total'] = top_items_df['CA Total'].apply(lambda x: f"£{x:,.2f}")
    st.dataframe(top_items_df, use_container_width=True, hide_index=True)

    # Vue d'ensemble des segments
    st.subheader("Métriques par Segment")
    segments_metrics = get_all_segments_metrics(df, rfm)
    segments_metrics['CA'] = segments_metrics['CA'].apply(lambda x: f"£{x:,.2f}")
    segments_metrics['Panier Moyen'] = segments_metrics['Panier Moyen'].apply(lambda x: f"£{x:,.2f}")
    st.dataframe(segments_metrics, use_container_width=True, hide_index=True)

    # Graphique de distribution des segments
    st.subheader("Distribution des Clients par Segment")
    segment_counts = rfm['Segment'].value_counts().reset_index()
    segment_counts.columns = ['Segment', 'Nombre de Clients']
    fig = px.pie(segment_counts, names='Segment', values='Nombre de Clients',
                 title='Répartition des Clients par Segment')
    st.plotly_chart(fig, use_container_width=True)

# ========== ONGLET 2: VUE PAR SEGMENT ==========
with tabs[1]:
    st.header("Vue par Segment")

    # Sélecteur de segment
    segments = sorted(rfm['Segment'].unique())
    selected_segment = st.selectbox("Sélectionnez un Segment", segments)

    if selected_segment:
        # Métriques du segment
        segment_metrics = compute_segment_metrics(df, rfm, selected_segment)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("CA du Segment", f"£{segment_metrics['ca_total']:,.2f}")
        with col2:
            st.metric("Panier Moyen", f"£{segment_metrics['panier_moyen']:,.2f}")
        with col3:
            st.metric("Nombre de Commandes", f"{segment_metrics['nb_commandes']:,}")

        # Nombre de clients dans le segment
        nb_clients_segment = len(rfm[rfm['Segment'] == selected_segment])
        st.metric("Nombre de Clients dans le Segment", f"{nb_clients_segment:,}")

        # Top 5 items pour ce segment
        st.subheader(f"Top 5 Items Achetés dans le Segment '{selected_segment}'")
        if len(segment_metrics['top_items']) > 0:
            top_items_segment_df = segment_metrics['top_items'].reset_index()
            top_items_segment_df.columns = ['Produit', 'CA Total']
            top_items_segment_df['CA Total'] = top_items_segment_df['CA Total'].apply(lambda x: f"£{x:,.2f}")
            st.dataframe(top_items_segment_df, use_container_width=True, hide_index=True)
        else:
            st.info("Aucune donnée disponible pour ce segment")

        # Profil RFM moyen du segment
        st.subheader(f"Profil RFM Moyen du Segment '{selected_segment}'")
        segment_profile = rfm[rfm['Segment'] == selected_segment][['Recency', 'Frequency', 'Monetary']].mean()
        profile_df = pd.DataFrame({
            'Métrique': ['Recency (jours)', 'Frequency (commandes)', 'Monetary (£)'],
            'Valeur Moyenne': [
                f"{segment_profile['Recency']:.1f}",
                f"{segment_profile['Frequency']:.1f}",
                f"£{segment_profile['Monetary']:,.2f}"
            ]
        })
        st.dataframe(profile_df, use_container_width=True, hide_index=True)

# ========== ONGLET 3: RECOMMANDATIONS PRODUIT ==========
with tabs[2]:
    st.header("Recommandations Produit")

    # Sélecteur de client
    customer_ids = sorted(rfm.index)
    selected_customer = st.selectbox("Sélectionnez un Client", customer_ids, key='customer_select')

    if selected_customer:
        # Informations client
        st.subheader(f"Informations Client: {selected_customer}")
        customer_segment = rfm.loc[selected_customer, 'Segment']
        customer_rfm = rfm.loc[selected_customer][['Recency', 'Frequency', 'Monetary']]

        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Segment:** {customer_segment}")
            st.write(f"**Recency:** {customer_rfm['Recency']:.0f} jours")
        with col2:
            st.write(f"**Frequency:** {customer_rfm['Frequency']:.0f} commandes")
            st.write(f"**Monetary:** £{customer_rfm['Monetary']:,.2f}")

        # Achats précédents
        st.subheader("Achats Précédents")
        customer_history = df[df['CustomerID'] == selected_customer][['InvoiceDate', 'Description', 'Quantity', 'TotalPrice']]
        customer_history = customer_history.sort_values('InvoiceDate', ascending=False)
        customer_history['TotalPrice'] = customer_history['TotalPrice'].apply(lambda x: f"£{x:,.2f}")
        st.dataframe(customer_history.head(10), use_container_width=True, hide_index=True)

        # Produits uniques achetés
        unique_products = df[df['CustomerID'] == selected_customer]['Description'].nunique()
        st.write(f"**Nombre de produits uniques achetés:** {unique_products}")

        # Recommandations avec lift
        st.subheader("Recommandations Produit")
        recs_data = get_customer_recommendations(df, rfm, rules, selected_customer)

        if len(recs_data['recommendations']) > 0:
            recs_df = pd.DataFrame(recs_data['recommendations'])
            # Formater le lift et confidence
            recs_df['lift'] = recs_df['lift'].apply(lambda x: f"{x:.2f}" if x is not None else "N/A")
            recs_df['confidence'] = recs_df['confidence'].apply(lambda x: f"{x:.2f}" if x is not None else "N/A")
            recs_df.columns = ['Produit', 'Lift', 'Confidence', 'Source']
            st.dataframe(recs_df, use_container_width=True, hide_index=True)

            # Explication du lift
            st.info("""
            **Interprétation du Lift:**
            - Lift > 1: Les produits sont souvent achetés ensemble (recommandation forte)
            - Lift = 1: Aucune corrélation
            - Lift < 1: Les produits sont rarement achetés ensemble
            - N/A: Recommandation basée sur la popularité du segment
            """)
        else:
            st.warning("Aucune recommandation disponible pour ce client")