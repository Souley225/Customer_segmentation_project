"""
Application Streamlit - Tableau de Bord Segmentation Client
Dashboard business pour stakeholders et managers
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.data_preprocessing import load_and_clean_data
from src.rfm_analysis import calculate_rfm, score_rfm, map_rfm_to_segment
from src.basket_analysis import perform_basket_analysis
from src.recommendations import get_customer_recommendations
from src.metrics import (
    compute_global_metrics, 
    compute_segment_metrics, 
    get_all_segments_metrics,
    compute_business_insights,
    get_segment_actions
)

# Configuration
st.set_page_config(
    page_title="Segmentation Client",
    page_icon="chart_with_upwards_trend",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS professionnel
st.markdown("""
<style>
    /* Header */
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a2e;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #4361ee;
        margin-bottom: 1.5rem;
    }
    
    .section-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #16213e;
        margin: 1.2rem 0 0.8rem 0;
        padding-left: 0.5rem;
        border-left: 4px solid #4361ee;
    }
    
    /* KPI Cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%);
        padding: 0.8rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(67, 97, 238, 0.3);
    }
    
    [data-testid="stMetric"] label {
        color: rgba(255,255,255,0.85) !important;
        font-size: 0.85rem;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: white !important;
        font-weight: 700;
        font-size: 1.4rem;
    }
    
    /* Alert Cards */
    .alert-card {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .alert-critical {
        background: linear-gradient(135deg, #ef476f 0%, #c1121f 100%);
        color: white;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #ffd166 0%, #f77f00 100%);
        color: #1a1a2e;
    }
    
    .alert-success {
        background: linear-gradient(135deg, #06d6a0 0%, #118ab2 100%);
        color: white;
    }
    
    .alert-info {
        background: linear-gradient(135deg, #4cc9f0 0%, #4361ee 100%);
        color: white;
    }
    
    /* Insight Box */
    .insight-box {
        background: #f8f9fa;
        border-left: 4px solid #4361ee;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.8rem 0;
    }
    
    .insight-title {
        font-weight: 600;
        color: #1a1a2e;
        margin-bottom: 0.3rem;
    }
    
    /* Tables */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #f0f2f5;
        padding: 0.4rem;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 6px;
        font-weight: 500;
        padding: 0.4rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%);
        color: white;
    }
    
    /* Priority badges */
    .priority-critique { color: #ef476f; font-weight: 700; }
    .priority-haute { color: #f77f00; font-weight: 600; }
    .priority-moyenne { color: #4361ee; font-weight: 500; }
    .priority-basse { color: #6c757d; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">Tableau de Bord Segmentation Client</p>', unsafe_allow_html=True)

# Chargement des données (pré-calculées ou calcul à la volée)
@st.cache_data
def load_app_data():
    """
    Chargement des données pré-calculées pour un démarrage rapide.
    Fallback sur calcul complet si les fichiers n'existent pas.
    """
    import os
    import pickle
    
    processed_dir = os.path.join(os.path.dirname(__file__), 'data', 'processed')
    transactions_path = os.path.join(processed_dir, 'transactions.csv')
    rfm_path = os.path.join(processed_dir, 'rfm_segments.csv')
    rules_path = os.path.join(processed_dir, 'association_rules.pkl')
    
    # Vérifier si les fichiers pré-calculés existent
    if all(os.path.exists(p) for p in [transactions_path, rfm_path, rules_path]):
        # Chargement rapide des données pré-calculées
        df = pd.read_csv(transactions_path, parse_dates=['InvoiceDate'])
        rfm = pd.read_csv(rfm_path, index_col='CustomerID')
        with open(rules_path, 'rb') as f:
            rules = pickle.load(f)
        return df, rfm, rules
    
    # Fallback: calcul complet (première exécution ou données manquantes)
    from src.data_preprocessing import load_and_clean_data
    from src.rfm_analysis import calculate_rfm, score_rfm, map_rfm_to_segment
    from src.basket_analysis import perform_basket_analysis
    
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

# Onglets principaux
tabs = st.tabs([
    'Synthese Executive',
    'Performance Segments', 
    'Actions Prioritaires',
    'Client 360'
])

# ========== ONGLET 1: SYNTHESE EXECUTIVE ==========
with tabs[0]:
    # KPIs globaux
    global_metrics = compute_global_metrics(df)
    insights = compute_business_insights(df, rfm)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Chiffre d'Affaires", f"£{global_metrics['ca_total']:,.0f}")
    with col2:
        st.metric("Clients Actifs", f"{global_metrics['nb_clients']:,}")
    with col3:
        st.metric("Panier Moyen", f"£{global_metrics['panier_moyen']:,.0f}")
    with col4:
        st.metric("Valeur Client Moyenne", f"£{insights['valeur_client_moyenne']:,.0f}")
    
    st.markdown("---")
    
    # Alertes et insights
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.markdown('<p class="section-header">Alertes Business</p>', unsafe_allow_html=True)
        
        # Clients à risque
        if insights['nb_clients_risque'] > 0:
            st.markdown(f"""
            <div class="alert-card alert-critical">
                <strong>{insights['nb_clients_risque']} clients haute valeur à risque</strong><br>
                Représentent £{insights['ca_risque']:,.0f} ({insights['pct_ca_risque']:.1f}% du CA)
            </div>
            """, unsafe_allow_html=True)
        
        # Opportunités
        if insights['nb_opportunites'] > 0:
            st.markdown(f"""
            <div class="alert-card alert-success">
                <strong>{insights['nb_opportunites']} opportunités de développement</strong><br>
                Clients avec potentiel inexploité
            </div>
            """, unsafe_allow_html=True)
        
        # Taux rétention
        if insights['taux_retention'] < 50:
            st.markdown(f"""
            <div class="alert-card alert-warning">
                <strong>Taux de rétention : {insights['taux_retention']:.0f}%</strong><br>
                Clients actifs (achat dans les 90 derniers jours)
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-card alert-info">
                <strong>Taux de rétention : {insights['taux_retention']:.0f}%</strong><br>
                Clients actifs (achat dans les 90 derniers jours)
            </div>
            """, unsafe_allow_html=True)
    
    with col_right:
        st.markdown('<p class="section-header">Indicateurs Cles</p>', unsafe_allow_html=True)
        
        # Concentration CA
        st.markdown(f"""
        <div class="insight-box">
            <div class="insight-title">Concentration du CA (Regle 80/20)</div>
            {insights['concentration_80_20']:.1f}% des clients generent 80% du CA ({insights['nb_clients_80_pct']} clients)
        </div>
        """, unsafe_allow_html=True)
        
        # Top segment
        st.markdown(f"""
        <div class="insight-box">
            <div class="insight-title">Segment Leader</div>
            <strong>{insights['top_segment']}</strong> : {insights['top_segment_pct']:.1f}% du CA total
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Graphiques
    col_chart1, col_chart2 = st.columns([1, 1])
    
    with col_chart1:
        st.markdown('<p class="section-header">Repartition du CA par Segment</p>', unsafe_allow_html=True)
        segments_metrics = get_all_segments_metrics(df, rfm)
        fig_ca = px.bar(
            segments_metrics,
            x='Segment',
            y='CA',
            color='Segment',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_ca.update_layout(
            showlegend=False,
            margin=dict(t=10, b=10, l=10, r=10),
            height=300,
            xaxis_title="",
            yaxis_title="CA (£)"
        )
        st.plotly_chart(fig_ca, use_container_width=True)
    
    with col_chart2:
        st.markdown('<p class="section-header">Distribution Clients vs CA</p>', unsafe_allow_html=True)
        fig_comparison = go.Figure()
        fig_comparison.add_trace(go.Bar(
            name='Part Clients (%)',
            x=segments_metrics['Segment'],
            y=segments_metrics['Part Clients'],
            marker_color='#4361ee'
        ))
        fig_comparison.add_trace(go.Bar(
            name='Part CA (%)',
            x=segments_metrics['Segment'],
            y=segments_metrics['Part CA'],
            marker_color='#06d6a0'
        ))
        fig_comparison.update_layout(
            barmode='group',
            margin=dict(t=10, b=10, l=10, r=10),
            height=300,
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            xaxis_title="",
            yaxis_title="%"
        )
        st.plotly_chart(fig_comparison, use_container_width=True)

# ========== ONGLET 2: PERFORMANCE SEGMENTS ==========
with tabs[1]:
    st.markdown('<p class="section-header">Selection du Segment</p>', unsafe_allow_html=True)
    
    segments = sorted(rfm['Segment'].unique())
    selected_segment = st.selectbox("Segment", segments, label_visibility="collapsed")
    
    if selected_segment:
        segment_metrics = compute_segment_metrics(df, rfm, selected_segment)
        segment_data = rfm[rfm['Segment'] == selected_segment]
        nb_clients = len(segment_data)
        
        st.markdown(f"### {selected_segment}")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("CA Segment", f"£{segment_metrics['ca_total']:,.0f}")
        with col2:
            st.metric("Clients", f"{nb_clients:,}")
        with col3:
            st.metric("Panier Moyen", f"£{segment_metrics['panier_moyen']:,.0f}")
        with col4:
            valeur_client = segment_metrics['ca_total'] / nb_clients if nb_clients > 0 else 0
            st.metric("Valeur par Client", f"£{valeur_client:,.0f}")
        
        st.markdown("---")
        
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.markdown('<p class="section-header">Profil RFM du Segment</p>', unsafe_allow_html=True)
            profile = segment_data[['Récence', 'Fréquence', 'Montant']].mean()
            profile_df = pd.DataFrame({
                'Indicateur': ['Récence', 'Fréquence', 'Montant'],
                'Valeur Moyenne': [
                    f"{profile['Récence']:.0f} jours",
                    f"{profile['Fréquence']:.1f}",
                    f"£{profile['Montant']:,.0f}"
                ],
                'Interpretation': [
                    'Faible = actif' if profile['Récence'] < 60 else 'Elevé = inactif',
                    'Elevée = engagement fort' if profile['Fréquence'] > 3 else 'Faible = occasionnel',
                    'Elevé = haute valeur' if profile['Montant'] > 500 else 'Standard'
                ]
            })
            st.dataframe(profile_df, use_container_width=True, hide_index=True)
            
            # Distribution RFM
            fig_rfm = go.Figure()
            fig_rfm.add_trace(go.Scatterpolar(
                r=[profile['Récence']/segment_data['Récence'].max()*100, 
                   profile['Fréquence']/segment_data['Fréquence'].max()*100, 
                   profile['Montant']/segment_data['Montant'].max()*100],
                theta=['Récence', 'Fréquence', 'Montant'],
                fill='toself',
                name=selected_segment,
                line_color='#4361ee'
            ))
            fig_rfm.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=False,
                margin=dict(t=30, b=30, l=30, r=30),
                height=250
            )
            st.plotly_chart(fig_rfm, use_container_width=True)
        
        with col_right:
            st.markdown('<p class="section-header">Top Produits du Segment</p>', unsafe_allow_html=True)
            if len(segment_metrics['top_items']) > 0:
                top_df = segment_metrics['top_items'].reset_index()
                top_df.columns = ['Produit', 'CA']
                top_df['CA'] = top_df['CA'].apply(lambda x: f"£{x:,.0f}")
                st.dataframe(top_df, use_container_width=True, hide_index=True)
            
            # Actions recommandées
            actions = get_segment_actions(selected_segment)
            st.markdown('<p class="section-header">Actions Recommandees</p>', unsafe_allow_html=True)
            priority_class = f"priority-{actions['priorite'].lower()}"
            st.markdown(f"""
            <div class="insight-box">
                <div class="insight-title">Priorité : <span class="{priority_class}">{actions['priorite']}</span></div>
                <strong>{actions['action']}</strong><br>
                {actions['tactique']}
            </div>
            """, unsafe_allow_html=True)

# ========== ONGLET 3: ACTIONS PRIORITAIRES ==========
with tabs[2]:
    st.markdown('<p class="section-header">Matrice des Actions par Segment</p>', unsafe_allow_html=True)
    
    # Tableau des actions
    segments_metrics = get_all_segments_metrics(df, rfm)
    actions_data = []
    for segment in segments_metrics['Segment']:
        actions = get_segment_actions(segment)
        seg_data = segments_metrics[segments_metrics['Segment'] == segment].iloc[0]
        actions_data.append({
            'Segment': segment,
            'Clients': int(seg_data['Clients']),
            'CA': f"£{seg_data['CA']:,.0f}",
            'Priorité': actions['priorite'],
            'Action': actions['action'],
            'Tactique': actions['tactique']
        })
    
    actions_df = pd.DataFrame(actions_data)
    
    # Tri par priorité
    priority_order = {'Critique': 0, 'Haute': 1, 'Moyenne': 2, 'Basse': 3}
    actions_df['_sort'] = actions_df['Priorité'].map(priority_order)
    actions_df = actions_df.sort_values('_sort').drop('_sort', axis=1)
    
    st.dataframe(actions_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Focus clients à risque
    st.markdown('<p class="section-header">Clients Haute Valeur a Risque</p>', unsafe_allow_html=True)
    
    high_value = rfm['Montant'].quantile(0.75)
    high_recency = rfm['Récence'].quantile(0.75)
    at_risk = rfm[(rfm['Montant'] >= high_value) & (rfm['Récence'] >= high_recency)]
    
    if len(at_risk) > 0:
        at_risk_display = at_risk[['Récence', 'Fréquence', 'Montant', 'Segment']].head(10).copy()
        at_risk_display['Récence'] = at_risk_display['Récence'].apply(lambda x: f"{x:.0f} jours")
        at_risk_display['Montant'] = at_risk_display['Montant'].apply(lambda x: f"£{x:,.0f}")
        at_risk_display.index.name = 'Client ID'
        st.dataframe(at_risk_display.reset_index(), use_container_width=True, hide_index=True)
        
        st.markdown(f"""
        <div class="alert-card alert-warning">
            <strong>Action immediate requise :</strong> Contacter ces {len(at_risk)} clients pour comprendre 
            leurs besoins et proposer des offres personnalisees de reactivation.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Aucun client haute valeur identifié comme à risque")

# ========== ONGLET 4: CLIENT 360 ==========
with tabs[3]:
    st.markdown('<p class="section-header">Selection du Client</p>', unsafe_allow_html=True)
    
    customer_ids = sorted(rfm.index)
    selected_customer = st.selectbox("Client", customer_ids, key='customer_select', label_visibility="collapsed")
    
    if selected_customer:
        customer_segment = rfm.loc[selected_customer, 'Segment']
        customer_rfm = rfm.loc[selected_customer][['Récence', 'Fréquence', 'Montant']]
        
        st.markdown(f"### Client {selected_customer}")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Segment", customer_segment)
        with col2:
            st.metric("Récence", f"{customer_rfm['Récence']:.0f} jours")
        with col3:
            st.metric("Fréquence", f"{customer_rfm['Fréquence']:.0f}")
        with col4:
            st.metric("Valeur Totale", f"£{customer_rfm['Montant']:,.0f}")
        
        st.markdown("---")
        
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.markdown('<p class="section-header">Historique Achats</p>', unsafe_allow_html=True)
            history = df[df['CustomerID'] == selected_customer][['InvoiceDate', 'Description', 'Quantity', 'TotalPrice']]
            history = history.sort_values('InvoiceDate', ascending=False).head(10).copy()
            history['TotalPrice'] = history['TotalPrice'].apply(lambda x: f"£{x:,.0f}")
            history.columns = ['Date', 'Produit', 'Qté', 'Montant']
            st.dataframe(history, use_container_width=True, hide_index=True)
            
            unique_products = df[df['CustomerID'] == selected_customer]['Description'].nunique()
            total_orders = df[df['CustomerID'] == selected_customer]['InvoiceNo'].nunique()
            st.markdown(f"**{unique_products}** produits uniques | **{total_orders}** commandes")
        
        with col_right:
            st.markdown('<p class="section-header">Recommandations Produit</p>', unsafe_allow_html=True)
            recs_data = get_customer_recommendations(df, rfm, rules, selected_customer)
            
            if len(recs_data['recommendations']) > 0:
                recs_df = pd.DataFrame(recs_data['recommendations'])
                recs_df['lift'] = recs_df['lift'].apply(lambda x: f"{x:.2f}" if x else "-")
                recs_df['confidence'] = recs_df['confidence'].apply(lambda x: f"{x:.0%}" if x else "-")
                recs_df.columns = ['Produit', 'Score', 'Confiance', 'Source']
                st.dataframe(recs_df, use_container_width=True, hide_index=True)
            else:
                st.info("Aucune recommandation disponible")
            
            # Action pour ce client
            actions = get_segment_actions(customer_segment)
            st.markdown('<p class="section-header">Action Recommandee</p>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="insight-box">
                <strong>{actions['action']}</strong><br>
                {actions['tactique']}
            </div>
            """, unsafe_allow_html=True)