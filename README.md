# 🧠 Projet Data Science : Segmentation Client et Recommandation Produit

## 🌟 Objectif du projet

L'objectif de ce projet est de construire **une application complète de segmentation client et de recommandation produits**, combinant deux approches de data science :

1. **Segmentation RFM (Recency, Frequency, Monetary)** pour identifier les profils de clients selon leur comportement d'achat.
2. **Analyse des paniers (Market Basket Analysis)** pour détecter les associations de produits et proposer des **recommandations de cross-sell / upsell**.

Ce projet se veut **reproductible et industrialisable**, avec une architecture modulaire, un code clair et commenté en français, et une interface utilisateur via **Streamlit** pour la mise en valeur des résultats.

---

## 🧹 Architecture du projet

```
customer_analytics_project/
│
├── config/
│   └── config.yaml                 # Fichier de configuration global (chemins, seuils, paramètres)
│
├── data/
│   ├── raw/                        # Données brutes (ex: Online Retail UCI)
│   ├── interim/                    # Données intermédiaires (nettoyées partiellement)
│   └── processed/                  # Données prêtes pour la modélisation (RFM + règles)
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb      # Nettoyage et préparation des données
│   ├── 02_rfm_segmentation.ipynb   # Calcul et visualisation de la segmentation RFM
│   ├── 03_market_basket_analysis.ipynb # Règles d'association (Apriori)
│   └── 04_dashboard_design.ipynb   # Tests et prototypage du dashboard Streamlit
│
├── src/
│   ├── data_cleaning.py            # Script de nettoyage complet (automatisé)
│   ├── rfm_segmentation.py         # Calcul des scores et classification RFM
│   ├── basket_analysis.py          # Génération des règles d'association
│   ├── recommendation.py           # Système de recommandation (cross-sell / upsell)
│   ├── visualization.py            # Graphiques interactifs
│   └── utils.py                    # Fonctions utilitaires (logs, config, etc.)
│
├── app/
│   ├── streamlit_app.py            # Application Streamlit principale
│   ├── components/                 # Widgets réutilisables
│   └── assets/                     # Images, logos, CSS
│
├── models/
│   ├── rfm_segments.csv            # Segmentation finale
│   ├── association_rules.csv       # Règles d'association extraites
│   └── metadata.json               # Informations sur les versions et hyperparamètres
│
├── reports/
│   └── figures/                    # Graphiques et visualisations
│
├── requirements.txt                # Dépendances Python
├── README.md                       # Présent document
└── app.py                          # Point d'entrée (redirection vers Streamlit)
```

---

## ⚙️ 1. Préparation et configuration

Avant de commencer :

```bash
# Créer et activer un environnement virtuel
python -m venv .venv
.venv\Scripts\activate      # (Windows)
source .venv/bin/activate   # (Linux / macOS)

# Installer les dépendances
pip install -r requirements.txt
```

Fichier `requirements.txt` minimal :

```
pandas
numpy
scikit-learn
mlxtend
plotly
streamlit
pyyaml
openpyxl
```

---

## 🧹 2. Nettoyage des données (`data_cleaning.py`)

### Description

Ce module gère le **prétraitement complet** des données. Il transforme les données brutes (Online Retail) en un jeu propre et exploitable pour les étapes suivantes.

### Étapes principales :

1. Suppression des transactions annulées.
2. Suppression des lignes avec `CustomerID` manquant.
3. Filtrage des valeurs négatives.
4. Normalisation du texte (`lowercase`).
5. Calcul de `TotalPrice`.
6. Export du dataset nettoyé.

---

## 📊 3. Segmentation RFM (`rfm_segmentation.py`)

### Description

On segmente les clients selon trois indicateurs :

* **Recency** : jours depuis le dernier achat
* **Frequency** : nombre total de commandes
* **Monetary** : total dépensé

### Étapes :

1. Calcul des indicateurs.
2. Attribution de scores 1-5 par quantiles.
3. Calcul d'un score global `RFM_Score`.
4. Classification des clients en segments.

---

## 🛍️ 4. Analyse des paniers (`basket_analysis.py`)

### Objectif

Identifier les produits les plus fréquemment achetés ensemble via **Apriori** et les **règles d'association**.

### Sorties attendues

* `association_rules.csv` avec : support, confiance, lift, produits.

---

## 🔮 5. Recommandations et Dashboard (`streamlit_app.py`)

### Objectif

Créer un tableau de bord interactif permettant :

* d'explorer les segments RFM,
* d'afficher les produits associés,
* de recommander des produits à un client ou segment.

### Commande de lancement :

```bash
streamlit run app/streamlit_app.py
```

Le dashboard comprendra :

* Page **Vue d'ensemble** : KPIs et métriques globales.
* Page **Segmentation RFM** : graphique interactif 3D.
* Page **Recommandations** : top 10 des associations produits.

---

## 🚀 6. Déploiement

* **Localement** : via `streamlit run app/streamlit_app.py`
* **Cloud** : Streamlit Cloud, Render, ou Docker.


---

## 🧬 7. Améliorations futures

* Intégrer FastAPI pour exposer une API de recommandation.
* Ajouter une base SQL (PostgreSQL) pour stocker les segments.


---

## 🌟 Résumé

Ce projet illustre le cycle complet d'un projet data orienté business :

* **Collecte & nettoyage** des données clients
* **Segmentation RFM** pour comprendre les comportements
* **Market Basket Analysis** pour détecter les opportunités de crossell et Upsell
* **Dashboard Streamlit** pour la visualisation et la décision

Ce README peut être suivi pas à pas pour reproduire le projet de A à Z, chaque script étant commenté en français pour servir de guide technique et pédagogique.
