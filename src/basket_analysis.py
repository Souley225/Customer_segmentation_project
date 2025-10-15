"""
Module d'analyse de panier
Extraction des règles d'ASSOCIATION OPTIMISÉE
"""
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from src.data_preprocessing import load_config

def perform_basket_analysis(df):
    """Analyse complète du panier OPTIMISÉE"""
    config = load_config()
    
    # ÉCHANTILLONNAGE : Top 1000 factures + Top 500 produits
    top_invoices = df['InvoiceNo'].value_counts().head(1000).index
    top_products = df['Description'].value_counts().head(500).index
    
    df_sample = df[df['InvoiceNo'].isin(top_invoices) & 
                   df['Description'].isin(top_products)]
    
    # Panier binaire OPTIMISÉ
    basket = (df_sample.groupby(['InvoiceNo', 'Description'])['Quantity']
              .sum().unstack().fillna(0)
              .map(lambda x: 1 if x > 0 else 0))  # ✅ map au lieu de applymap
    
    # Vérification mémoire
    if basket.shape[1] > 200:
        basket = basket.loc[:, basket.sum() > 10]  # Top produits fréquents
    
    frequent_itemsets = apriori(basket, 
                              min_support=0.05,  # ✅ Augmenté
                              use_colnames=True,
                              low_memory=True)   # ✅ Optimisé
    
    if frequent_itemsets.empty:
        return pd.DataFrame()
        
    rules = association_rules(frequent_itemsets, metric='lift',
                            min_threshold=1.2)  # ✅ Plus strict
    
    rules = rules[rules['confidence'] >= 0.3]  # ✅ Plus strict
    return rules.head(50)  # ✅ Limité