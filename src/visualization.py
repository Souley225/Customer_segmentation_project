"""
Module de visualisation
Fonctions de création des graphiques
"""
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import networkx as nx

def create_kpi_metrics(df, rfm):
    """KPIs principaux"""
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric('Total Clients', len(rfm))
    with col2: st.metric('Ventes Totales', f"£{df['TotalPrice'].sum():,.2f}")
    with col3: st.metric('Nb Commandes', df['InvoiceNo'].nunique())
    with col4: st.metric('Valeur Moyenne', f"£{df['TotalPrice'].sum()/df['InvoiceNo'].nunique():,.2f}")

def create_rfm_pie(rfm):
    """Graphique secteurs RFM"""
    segment_counts = rfm['Segment'].value_counts().reset_index()
    fig = px.pie(segment_counts, names='Segment', values='count', title='Distribution RFM')
    st.plotly_chart(fig, use_container_width=True)

def create_segment_profiles(rfm):
    """Profils moyens par segment"""
    profiles = rfm.groupby('Segment')[['Récence', 'Fréquence', 'Montant']].mean().round(2)
    st.dataframe(profiles, use_container_width=True)

def create_monetary_box(rfm):
    """Boîtes monétaires"""
    fig = px.box(rfm, x='Segment', y='Montant', title='Distribution Monétaire')
    st.plotly_chart(fig, use_container_width=True)

def create_evolution_area(evol_df):
    """Évolution segments"""
    fig = px.area(evol_df, x=evol_df.index, y=evol_df.columns, title='Évolution Segments')
    st.plotly_chart(fig, use_container_width=True)

def create_rules_table(rules):
    """Tableau règles"""
    top_rules = rules.sort_values('lift', ascending=False).head(10)
    st.dataframe(top_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

def create_support_confidence_scatter(rules):
    """Nuage support/confiance"""
    top_rules = rules.sort_values('lift', ascending=False).head(20)
    fig = px.scatter(top_rules, x='support', y='confidence', size='lift', title='Support vs Confiance')
    st.plotly_chart(fig, use_container_width=True)

def create_association_graph(rules):
    """Graphe associations"""
    G = nx.DiGraph()
    top_rules = rules.sort_values('lift', ascending=False).head(20)
    
    for _, row in top_rules.iterrows():
        for ante in row['antecedents']:
            for cons in row['consequents']:
                G.add_edge(ante, cons, weight=row['confidence'])
    
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, 
            edge_color='gray', font_size=8, arrows=True)
    st.pyplot(plt)