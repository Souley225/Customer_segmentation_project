"""
Page de vue détaillée d'un client individuel.
"""

import streamlit as st
import pandas as pd
from src.utils import load_config
from src.visualization import plot_customer_history

# Configuration
config = load_config()

st.set_page_config(
    page_title=f"{config['streamlit']['page_title']} - Vue Client",
    layout="wide"
)

def load_data():
    """Charge toutes les données nécessaires."""
    clean_data = pd.read_csv(
        config["paths"]["processed_data"],
        parse_dates=["InvoiceDate"]
    )
    rfm_data = pd.read_csv(config["paths"]["rfm_output"])
    recommendations = pd.read_csv(config["paths"]["recommendations"])
    
    return clean_data, rfm_data, recommendations

def get_customer_details(customer_id, data, rfm_data):
    """Récupère les détails d'un client spécifique."""
    customer_transactions = data[data["CustomerID"] == customer_id]
    customer_rfm = rfm_data[rfm_data["CustomerID"] == customer_id].iloc[0]
    
    details = {
        "Nombre de commandes": len(customer_transactions["InvoiceNo"].unique()),
        "Montant total dépensé": customer_transactions["TotalPrice"].sum(),
        "Panier moyen": customer_transactions.groupby("InvoiceNo")["TotalPrice"].sum().mean(),
        "Première commande": customer_transactions["InvoiceDate"].min(),
        "Dernière commande": customer_transactions["InvoiceDate"].max(),
        "Segment": customer_rfm["Segment"],
        "Score Recency": customer_rfm["Recency"],
        "Score Frequency": customer_rfm["Frequency"],
        "Score Monetary": customer_rfm["Monetary"]
    }
    
    return details

def display_customer_transactions(data, customer_id):
    """Affiche l'historique des transactions d'un client."""
    transactions = data[data["CustomerID"] == customer_id].copy()
    transactions = transactions.sort_values("InvoiceDate", ascending=False)
    
    # Grouper par facture
    for invoice in transactions["InvoiceNo"].unique():
        invoice_items = transactions[transactions["InvoiceNo"] == invoice]
        
        with st.expander(
            f"Facture {invoice} - {invoice_items['InvoiceDate'].iloc[0].strftime('%d/%m/%Y')}"
        ):
            total = invoice_items["TotalPrice"].sum()
            st.write(f"**Total: {total:.2f} {config['streamlit']['currency']}**")
            
            # Afficher les articles
            items_df = invoice_items[["Description", "Quantity", "UnitPrice", "TotalPrice"]]
            items_df = items_df.rename(columns={
                "Description": "Article",
                "Quantity": "Quantité",
                "UnitPrice": "Prix unitaire",
                "TotalPrice": "Total"
            })
            st.dataframe(items_df)

def main():
    """Fonction principale de la vue client."""
    st.title("Vue Client Détaillée")
    
    try:
        # Charger les données
        data, rfm_data, recommendations = load_data()
        
        # Sélection du client
        customers = sorted(data["CustomerID"].unique())
        customer_id = st.selectbox(
            "Sélectionner un client",
            customers,
            format_func=lambda x: f"Client {x}"
        )
        
        if customer_id:
            # Récupérer les détails du client
            details = get_customer_details(customer_id, data, rfm_data)
            
            # Afficher les métriques principales
            st.header(f"Profil du client {customer_id}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Segment",
                    details["Segment"]
                )
                st.metric(
                    "Nombre de commandes",
                    f"{details['Nombre de commandes']}"
                )
                
            with col2:
                st.metric(
                    "Montant total dépensé",
                    f"{details['Montant total dépensé']:.2f} {config['streamlit']['currency']}"
                )
                st.metric(
                    "Panier moyen",
                    f"{details['Panier moyen']:.2f} {config['streamlit']['currency']}"
                )
                
            with col3:
                st.metric(
                    "Première commande",
                    details["Première commande"].strftime("%d/%m/%Y")
                )
                st.metric(
                    "Dernière commande",
                    details["Dernière commande"].strftime("%d/%m/%Y")
                )
            
            # Scores RFM
            st.header("Scores RFM")
            rfm_col1, rfm_col2, rfm_col3 = st.columns(3)
            
            with rfm_col1:
                st.metric("Récence", f"{details['Score Recency']:.1f}")
            with rfm_col2:
                st.metric("Fréquence", f"{details['Score Frequency']:.1f}")
            with rfm_col3:
                st.metric("Monétaire", f"{details['Score Monetary']:.1f}")
            
            # Graphique d'historique
            st.header("Historique des achats")
            fig = plot_customer_history(data, customer_id, config)
            st.plotly_chart(fig, use_container_width=True)
            
            # Recommandations
            st.header("Produits recommandés")
            customer_recs = recommendations[
                recommendations["CustomerID"] == customer_id
            ].iloc[0]
            
            rec_cols = st.columns(config["recommendation"]["n_recommendations"])
            for i, col in enumerate(rec_cols, 1):
                with col:
                    st.write(f"**{i}.**")
                    st.write(customer_recs[f"Recommendation_{i}"])
            
            # Historique détaillé
            st.header("Détail des transactions")
            display_customer_transactions(data, customer_id)
            
            # Export des données
            st.sidebar.header("Exporter les données")
            
            if st.sidebar.button("Télécharger profil client"):
                customer_data = data[data["CustomerID"] == customer_id]
                customer_data.to_csv("temp_customer_export.csv", index=False)
                with open("temp_customer_export.csv", "rb") as file:
                    st.sidebar.download_button(
                        "Confirmer le téléchargement",
                        file,
                        f"client_{customer_id}.csv",
                        "text/csv"
                    )
        
    except Exception as e:
        st.error(f"Une erreur s'est produite: {str(e)}")
        st.error("Vérifiez que les fichiers de données existent et sont accessibles.")

if __name__ == "__main__":
    main()