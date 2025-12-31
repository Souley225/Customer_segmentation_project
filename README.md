# Segmentation Client & Recommandation Produit

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

---

## Licence

MIT
