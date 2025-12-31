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
    page_title="Segmentation Client",
    page_icon="chart_with_upwards_trend",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé pour un look HR-friendly
st.markdown("""
<style>
    /* Header principal */
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e3a5f;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3498db;
        margin-bottom: 1.5rem;
    }
    
    /* Sous-titres */
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding-left: 0.5rem;
        border-left: 4px solid #3498db;
    }
    
    /* Cartes métriques */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    [data-testid="stMetric"] label {
        color: rgba(255,255,255,0.9) !important;
        font-weight: 500;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: white !important;
        font-weight: 700;
    }
    
    /* Tableaux */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    
    /* Onglets */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8f9fa;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Info boxes */
    .info-box {
        background: #e8f4fd;
        border-left: 4px solid #3498db;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown('<p class="main-header">Tableau de Bord Segmentation Client</p>', unsafe_allow_html=True)

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
tabs = st.tabs([
    'Vue Globale',
    'Analyse par Segment', 
    'Recommandations Client'
])

# ========== ONGLET 1: VUE GLOBALE DES SEGMENTS ==========
with tabs[0]:
    st.markdown('<p class="section-header">Performance Globale</p>', unsafe_allow_html=True)

    # Métriques globales
    global_metrics = compute_global_metrics(df)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Chiffre d'Affaires Total", f"£{global_metrics['ca_total']:,.0f}")
    with col2:
        st.metric("Panier Moyen", f"£{global_metrics['panier_moyen']:,.0f}")
    with col3:
        st.metric("Nombre de Commandes", f"{global_metrics['nb_commandes']:,}")

    st.markdown("---")
    
    # Layout en 2 colonnes
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        # Top 5 items achetés
        st.markdown('<p class="section-header">Top 5 Produits par CA</p>', unsafe_allow_html=True)
        top_items_df = global_metrics['top_items'].reset_index()
        top_items_df.columns = ['Produit', 'CA']
        top_items_df['CA'] = top_items_df['CA'].apply(lambda x: f"£{x:,.0f}")
        st.dataframe(top_items_df, use_container_width=True, hide_index=True)

    with col_right:
        # Graphique de distribution des segments
        st.markdown('<p class="section-header">Répartition des Clients</p>', unsafe_allow_html=True)
        segment_counts = rfm['Segment'].value_counts().reset_index()
        segment_counts.columns = ['Segment', 'Clients']
        fig = px.pie(
            segment_counts, 
            names='Segment', 
            values='Clients',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    # Vue d'ensemble des segments
    st.markdown('<p class="section-header">Performance par Segment</p>', unsafe_allow_html=True)
    segments_metrics = get_all_segments_metrics(df, rfm)
    segments_metrics['CA'] = segments_metrics['CA'].apply(lambda x: f"£{x:,.0f}")
    segments_metrics['Panier Moyen'] = segments_metrics['Panier Moyen'].apply(lambda x: f"£{x:,.0f}")
    st.dataframe(segments_metrics, use_container_width=True, hide_index=True)

# ========== ONGLET 2: VUE PAR SEGMENT ==========
with tabs[1]:
    st.markdown('<p class="section-header">Sélection du Segment</p>', unsafe_allow_html=True)

    # Sélecteur de segment
    segments = sorted(rfm['Segment'].unique())
    selected_segment = st.selectbox("Choisir un segment à analyser", segments, label_visibility="collapsed")

    if selected_segment:
        # Métriques du segment
        segment_metrics = compute_segment_metrics(df, rfm, selected_segment)
        
        st.markdown(f"### Segment : {selected_segment}")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("CA du Segment", f"£{segment_metrics['ca_total']:,.0f}")
        with col2:
            st.metric("Panier Moyen", f"£{segment_metrics['panier_moyen']:,.0f}")
        with col3:
            st.metric("Commandes", f"{segment_metrics['nb_commandes']:,}")
        with col4:
            nb_clients_segment = len(rfm[rfm['Segment'] == selected_segment])
            st.metric("Clients", f"{nb_clients_segment:,}")

        st.markdown("---")
        
        # Layout en 2 colonnes
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            # Top 5 items pour ce segment
            st.markdown('<p class="section-header">Top 5 Produits du Segment</p>', unsafe_allow_html=True)
            if len(segment_metrics['top_items']) > 0:
                top_items_segment_df = segment_metrics['top_items'].reset_index()
                top_items_segment_df.columns = ['Produit', 'CA']
                top_items_segment_df['CA'] = top_items_segment_df['CA'].apply(lambda x: f"£{x:,.0f}")
                st.dataframe(top_items_segment_df, use_container_width=True, hide_index=True)
            else:
                st.info("Aucune donnée disponible pour ce segment")

        with col_right:
            # Profil RFM moyen du segment
            st.markdown('<p class="section-header">Profil RFM Moyen</p>', unsafe_allow_html=True)
            segment_profile = rfm[rfm['Segment'] == selected_segment][['Récence', 'Fréquence', 'Montant']].mean()
            profile_df = pd.DataFrame({
                'Indicateur': ['Récence', 'Fréquence', 'Montant'],
                'Description': [
                    'Jours depuis dernier achat',
                    'Nombre de commandes',
                    'Valeur totale dépensée'
                ],
                'Valeur': [
                    f"{segment_profile['Récence']:.0f} jours",
                    f"{segment_profile['Fréquence']:.0f} commandes",
                    f"£{segment_profile['Montant']:,.0f}"
                ]
            })
            st.dataframe(profile_df, use_container_width=True, hide_index=True)

# ========== ONGLET 3: RECOMMANDATIONS PRODUIT ==========
with tabs[2]:
    st.markdown('<p class="section-header">Sélection du Client</p>', unsafe_allow_html=True)

    # Sélecteur de client
    customer_ids = sorted(rfm.index)
    selected_customer = st.selectbox(
        "Choisir un client", 
        customer_ids, 
        key='customer_select',
        label_visibility="collapsed"
    )

    if selected_customer:
        # Informations client
        customer_segment = rfm.loc[selected_customer, 'Segment']
        customer_rfm = rfm.loc[selected_customer][['Récence', 'Fréquence', 'Montant']]
        
        st.markdown(f"### Client : {selected_customer}")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Segment", customer_segment)
        with col2:
            st.metric("Récence", f"{customer_rfm['Récence']:.0f} jours")
        with col3:
            st.metric("Fréquence", f"{customer_rfm['Fréquence']:.0f}")
        with col4:
            st.metric("Montant", f"£{customer_rfm['Montant']:,.0f}")

        st.markdown("---")
        
        # Layout en 2 colonnes
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            # Achats précédents
            st.markdown('<p class="section-header">Historique d\'Achats Récent</p>', unsafe_allow_html=True)
            customer_history = df[df['CustomerID'] == selected_customer][['InvoiceDate', 'Description', 'Quantity', 'TotalPrice']]
            customer_history = customer_history.sort_values('InvoiceDate', ascending=False)
            customer_history_display = customer_history.head(8).copy()
            customer_history_display['TotalPrice'] = customer_history_display['TotalPrice'].apply(lambda x: f"£{x:,.0f}")
            customer_history_display.columns = ['Date', 'Produit', 'Qté', 'Montant']
            st.dataframe(customer_history_display, use_container_width=True, hide_index=True)

            # Produits uniques achetés
            unique_products = df[df['CustomerID'] == selected_customer]['Description'].nunique()
            st.markdown(f"**Produits uniques achetés :** {unique_products}")

        with col_right:
            # Recommandations avec lift
            st.markdown('<p class="section-header">Recommandations Produit</p>', unsafe_allow_html=True)
            recs_data = get_customer_recommendations(df, rfm, rules, selected_customer)

            if len(recs_data['recommendations']) > 0:
                recs_df = pd.DataFrame(recs_data['recommendations'])
                recs_df['lift'] = recs_df['lift'].apply(lambda x: f"{x:.2f}" if x is not None else "-")
                recs_df['confidence'] = recs_df['confidence'].apply(lambda x: f"{x:.0%}" if x is not None else "-")
                recs_df.columns = ['Produit', 'Pertinence', 'Confiance', 'Source']
                st.dataframe(recs_df, use_container_width=True, hide_index=True)

                st.markdown("""
                <div class="info-box">
                <strong>Lecture des indicateurs :</strong><br>
                <strong>Pertinence (Lift)</strong> : Plus le score est élevé, plus l'association est forte<br>
                <strong>Confiance</strong> : Probabilité d'achat conjoint
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Aucune recommandation disponible pour ce client")