# Projet de Segmentation Client et Recommandation Produit
## Contexte et Objectif

Ce projet a pour but d'analyser le comportement des clients (achats, fréquence, montant) afin de réaliser une segmentation via la méthode RFM (Récence, Fréquence, Montant), puis d'utiliser l'analyse de panier (association rules) pour recommander des produits pertinents. Une interface Streamlit permet d'explorer les résultats de façon interactive.

 L'objectif est double :

Comprendre les profils clients et identifier les plus précieux (fidèles, gros acheteurs, etc.)

Générer des recommandations produits basées sur leurs habitudes d'achat

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange?logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**Application en ligne**: [customer-segmentation-project-591h.onrender.com](https://customer-segmentation-project-591h.onrender.com/)

---

## Contexte Business

Solution d'analytics retail transformant les données transactionnelles en insights clients actionnables via segmentation automatisée et recommandations intelligentes.

**Valeur Business:**
- Identification de la valeur client via scoring RFM
- Opportunités de cross-sell par analyse de panier
- Personnalisation data-driven à grande échelle

---

## Approche Technique

| Composant | Méthode | Résultat |
|-----------|---------|----------|
| **Segmentation** | Analyse RFM (Récence, Fréquence, Montant) | 4 segments clients |
| **Règles d'Association** | Algorithme Apriori | Affinités produits avec scores lift |
| **Recommandations** | Hybride (Association + Segment) | Top-N suggestions personnalisées |

---

## Fonctionnalités

- **Dashboard Exécutif** — KPIs: CA, panier moyen, volume commandes, top produits par segment
- **Analyse par Segment** — Métriques filtrées et profils RFM par segment client
- **Moteur de Recommandation** — Suggestions par client avec scores de confiance et sources

---

## Stack Technique

| Couche | Technologie |
|--------|-------------|
| Frontend | Streamlit |
| Traitement Données | Pandas |
| ML/Analytics | Scikit-learn, MLxtend (Apriori) |
| Visualisation | Plotly, NetworkX |
| Déploiement | Render |

---

## Source de Données

UCI Machine Learning Repository — [Online Retail Dataset](https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx)

**Schéma**: InvoiceNo, InvoiceDate, Description, Quantity, UnitPrice, CustomerID

---

## Structure du Projet

```
customer_segmentation_project/
├── app.py                  # Application Streamlit
├── src/
│   ├── data_preprocessing.py
│   ├── rfm_analysis.py
│   ├── basket_analysis.py
│   ├── recommendations.py
│   ├── metrics.py
│   └── visualization.py
├── config/
│   └── config.yaml         # Paramètres
├── requirements.txt
└── render.yaml              # Config déploiement
```

---

## Installation Rapide

```bash
git clone https://github.com/Souley225/customer_segmentation_project.git
cd customer_segmentation_project
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
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

## Contact
Pour questions ou suggestions, ouvrir une issue sur le repository GitHub.
Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue ou à nous contacter directement.
