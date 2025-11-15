# Projet de Segmentation Client et Recommandation Produit
## Contexte et Objectif

Ce projet a pour but d'analyser le comportement des clients (achats, fréquence, montant) afin de réaliser une segmentation via la méthode RFM (Récence, Fréquence, Montant), puis d'utiliser l'analyse de panier (association rules) pour recommander des produits pertinents. Une interface Streamlit permet d'explorer les résultats de façon interactive.

 L'objectif est double :

Comprendre les profils clients et identifier les plus précieux (fidèles, gros acheteurs, etc.)

Générer des recommandations produits basées sur leurs habitudes d'achat

## 🚀 Application Déployée

**Lien de l'application en ligne**: [https://customer-segmentation-project-591h.onrender.com/](https://customer-segmentation-project-591h.onrender.com/)

## Description
Application d'analyse client combinant segmentation RFM et analyse de panier pour fournir des insights commerciaux via une interface Streamlit.

## Fonctionnalités
- **Vue Globale des Segments**: CA total, panier moyen, nombre de commandes, top 5 items
- **Vue par Segment**: métriques détaillées par segment avec filtre
- **Recommandations Produit**: recommandations personnalisées avec lift pour chaque client
- **Segmentation RFM**: classification automatique des clients
- **Analyse de Panier**: règles d'association entre produits

## Structure du projet
```
customer_segmentation_project/
├── .streamlit/
│   └── config.toml
├── config/
│   ├── config.yaml
│   └── render.yaml
├── data/
│   └── processed/
├── src/
│   ├── __init__.py
│   ├── utils.py
│   ├── data_preprocessing.py
│   ├── rfm_analysis.py
│   ├── basket_analysis.py
│   ├── recommendations.py
│   ├── metrics.py
│   └── visualization.py
├── app.py
├── requirements.txt
└── README.md
```

## Prérequis
- Python 3.11
- Packages listés dans `requirements.txt`

## Installation Locale

1. Cloner le dépôt :
```bash
git clone https://github.com/Souley225/customer_segmentation_project.git
cd customer_segmentation_project
```

2. Créer un environnement virtuel :
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation Locale

Lancer l'application Streamlit :
```bash
streamlit run app.py
```

2. Lancer l'application Streamlit :
```bash
streamlit run app.py
```

- Les données sont chargées automatiquement depuis l'URL configurée dans `config/config.yaml`
- Aucune variable d'environnement secrète n'est requise
- Le fichier `.streamlit/config.toml` configure l'interface Streamlit
- L'application est optimisée pour fonctionner avec les ressources limitées de Render Free Tier

## Configuration

Le fichier `config/config.yaml` permet de configurer :
- **Source des données**: URL du fichier Excel Online Retail
- **Paramètres RFM**: quantiles pour Recency, Frequency, Monetary
- **Analyse de panier**: seuils de support, confidence, lift
- **Recommandations**: nombre de recommandations par source
- **Visualisation**: limites d'affichage

## Vues de l'Application

### 1. Vue Globale des Segments
- CA total et panier moyen
- Nombre total de commandes
- Top 5 items achetés (par CA)
- Tableau récapitulatif des métriques par segment
- Graphique de distribution des clients

### 2. Vue par Segment
- Sélection du segment via dropdown
- Métriques spécifiques au segment : CA, panier moyen, nombre de commandes
- Top 5 items du segment
- Profil RFM moyen du segment

### 3. Recommandations Produit
- Sélection du client via dropdown
- Informations client (segment, RFM)
- Historique d'achats détaillé
- Recommandations personnalisées avec :
  - Lift (pour règles d'association)
  - Confidence
  - Source de la recommandation (Association ou Segment)

## Structure des Données

### Source
Les données sont chargées depuis : [UCI Machine Learning Repository - Online Retail Dataset](https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx)

### Colonnes utilisées
- **InvoiceNo**: Numéro de facture
- **InvoiceDate**: Date de transaction
- **Description**: Description du produit
- **Quantity**: Quantité achetée
- **UnitPrice**: Prix unitaire
- **CustomerID**: Identifiant client
- **TotalPrice**: Calculé (Quantity × UnitPrice)

## Technologies Utilisées

- **Streamlit**: Framework web pour l'application
- **Pandas**: Manipulation des données
- **Scikit-learn**: Segmentation RFM
- **MLxtend**: Analyse de panier (Apriori, règles d'association)
- **Plotly**: Visualisations interactives
- **NetworkX**: Graphes d'association

## Performance et Optimisation

L'application est optimisée pour le déploiement cloud :
- Échantillonnage des données pour l'analyse de panier
- Cache Streamlit pour les calculs lourds
- Filtrage des règles d'association pour limiter la mémoire
- Chargement différé des visualisations

## Licence
Ce projet est sous licence MIT.

## Contact
Pour questions ou suggestions, ouvrir une issue sur le repository GitHub.
Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue ou à nous contacter directement.
