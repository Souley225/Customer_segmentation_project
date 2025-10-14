# Projet de Segmentation Client et Recommandation Produit

## Description
Application d'analyse client combinant segmentation RFM et analyse de panier pour fournir des insights commerciaux via une interface Streamlit.

## Fonctionnalités
- Segmentation RFM des clients
- Analyse des associations de produits
- Recommandations personnalisées
- Dashboard interactif avec Streamlit
- Export des données et visualisations

## Structure du projet
```
customer_segmentation_project/
├── config/
│   └── config.yaml
├── data/
│   ├── raw/
│   └── processed/
├── models/
├── logs/
├── src/
│   ├── utils.py
│   ├── data_preprocessing.py
│   ├── rfm_analysis.py
│   ├── basket_analysis.py
│   ├── recommendations.py
│   ├── visualization.py
│   └── main.py
├── streamlit_app/
│   ├── Home.py
│   └── pages/
│       ├── 02_Segmentation.py
│       ├── 03_Basket_Analysis.py
│       └── 04_Customer_View.py
└── tests/
```

## Prérequis
- Python 3.11
- Packages requis listés dans `requirements.txt`

## Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/votre-username/customer_segmentation_project.git
cd customer_segmentation_project
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Préparer les données :
- Placer le fichier `online_retail.csv` dans `data/raw/`
- Ajuster les paramètres dans `config/config.yaml` si nécessaire

## Utilisation

1. Exécuter le pipeline d'analyse :
```bash
python src/main.py
```

2. Lancer l'application Streamlit :
```bash
cd streamlit_app
streamlit run Home.py
```

L'application sera accessible à l'adresse : http://localhost:8501

## Configuration

Le fichier `config/config.yaml` permet de configurer :
- Les chemins des fichiers
- Les paramètres RFM
- Les seuils d'analyse de panier
- Les paramètres de recommandation
- L'apparence de l'interface Streamlit

## Structure des données

### Données d'entrée (`online_retail.csv`)
- InvoiceNo : Numéro de facture
- StockCode : Code produit
- Description : Description du produit
- Quantity : Quantité achetée
- InvoiceDate : Date de la transaction
- UnitPrice : Prix unitaire
- CustomerID : Identifiant client
- Country : Pays du client

### Données générées
- `clean_data.csv` : Données nettoyées
- `rfm_segments.csv` : Segmentation RFM
- `association_rules.csv` : Règles d'association
- `recommendations.csv` : Recommandations produits

## Visualisations disponibles
1. Vue globale :
   - KPIs principaux
   - Distribution RFM
   - Profils des segments

2. Analyse des segments :
   - Métriques par segment
   - Comparaisons inter-segments
   - Évolution temporelle

3. Analyse de panier :
   - Graphe des associations
   - Règles principales
   - Métriques de support/confiance

4. Vue client :
   - Profil RFM
   - Historique d'achat
   - Recommandations personnalisées

## Contribution
Les contributions sont les bienvenues ! Pour contribuer :
1. Forker le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Créer une Pull Request

## Licence
Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Contact
Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue ou à nous contacter directement.