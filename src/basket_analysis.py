"""
Module d'analyse de panier
Extraction des règles d'association
"""
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from src.data_preprocessing import load_config

def perform_basket_analysis(df):
    """Analyse complète du panier de marché"""
    config = load_config()
    
    basket = (df.groupby(['InvoiceNo', 'Description'])['Quantity']
              .sum().unstack().fillna(0)
              .applymap(lambda x: 1 if x > 0 else 0))
    
    frequent_itemsets = apriori(basket, 
                              min_support=config['basket_analysis']['min_support'], 
                              use_colnames=True)
    
    rules = association_rules(frequent_itemsets, metric='lift',
                            min_threshold=config['basket_analysis']['min_lift'])
    
    rules = rules[rules['confidence'] >= config['basket_analysis']['min_confidence']]
    return rules.head(config['basket_analysis']['max_rules'])