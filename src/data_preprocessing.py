"""
Module de préprocessing des données
Nettoyage, préparation et ingénierie des features
"""
import pandas as pd
import yaml
from datetime import datetime
import requests

from src.utils import load_config

def load_and_clean_data(source_url=None):
    """
    Chargement et nettoyage des données de vente en ligne
    """
    config = load_config()
    
    # Chargement depuis URL
    if source_url is None:
        source_url = config['data']['source_url']
    
    df = pd.read_excel(source_url)
    
    # Conversion des types
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['CustomerID'] = df['CustomerID'].astype('Int64')
    
    # Nettoyage
    if config['data']['drop_na_customer']:
        df = df.dropna(subset=['CustomerID'])
    
    df = df[df['Quantity'] > config['data']['min_quantity']]
    df = df[df['UnitPrice'] > 0]
    df = df.drop_duplicates()
    
    # Features
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    df['InvoiceMonth'] = df['InvoiceDate'].dt.to_period('M')
    
    return df