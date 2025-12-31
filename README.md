# Segmentation Client & Recommandation Produit

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange?logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**Application en ligne**: [customer-segmentation-project-591h.onrender.com](https://customer-segmentation-project-591h.onrender.com/)

[![Guide](https://img.shields.io/badge/Documentation-Guide_Utilisateur-purple?logo=bookstack&logoColor=white)](GUIDE_UTILISATEUR.md)

---

## Contexte Business

Solution d’analytics retail qui transforme les données transactionnelles en segments clients dynamiques et en recommandations opérationnelles, permettant d’optimiser le ciblage marketing, la fidélisation et le chiffre d’affaires.

**Valeur Business:**
- Identification de la valeur client via scoring RFM
- Detection des clients a risque et opportunites de croissance
- Recommandations cross-sell par analyse de panier
- Actions prioritaires par segment

---

## Fonctionnalites du Dashboard

| Onglet | Description |
|--------|-------------|
| **Synthese Executive** | KPIs globaux, alertes business, concentration 80/20 |
| **Performance Segments** | Profil RFM, radar chart, actions recommandees |
| **Actions Prioritaires** | Matrice d'actions, clients haute valeur a risque |
| **Client 360** | Vue individuelle, historique, recommandations produit |

---

## Approche Technique

| Composant | Methode | Output |
|-----------|---------|--------|
| **Segmentation** | Analyse RFM (Recence, Frequence, Montant) | 6 segments clients |
| **Regles d'Association** | Algorithme Apriori | Affinites produits avec lift |
| **Recommandations** | Hybride (Association + Segment) | Top-N suggestions personnalisees |

---

## Stack Technique

| Couche | Technologie |
|--------|-------------|
| Frontend | Streamlit |
| Traitement Donnees | Pandas |
| ML/Analytics | Scikit-learn, MLxtend (Apriori) |
| Visualisation | Plotly |
| Deploiement | Render |

---

## Structure du Projet

```
customer_segmentation_project/
├── app.py                      # Application Streamlit
├── scripts/
│   └── precompute.py           # Pre-calcul des donnees
├── src/
│   ├── data_preprocessing.py
│   ├── rfm_analysis.py
│   ├── basket_analysis.py
│   ├── recommendations.py
│   ├── metrics.py
│   └── visualization.py
├── data/
│   └── processed/              # Donnees pre-calculees
├── config/
│   └── config.yaml
├── requirements.txt
└── render.yaml
```

---

## Installation et Deploiement

### Installation Locale

```bash
git clone https://github.com/Souley225/customer_segmentation_project.git
cd customer_segmentation_project
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
```

### Workflow de Deploiement

```bash
# 1. Pre-calculer les donnees (execution locale)
python scripts/precompute.py

# 2. Commiter les fichiers pre-calcules
git add data/processed/
git commit -m "Mise a jour donnees pre-calculees"

# 3. Deployer
git push
```

Le pre-calcul reduit le temps de demarrage de ~60s a ~2s.

### Lancement Local

```bash
streamlit run app.py
```

---

## Source de Donnees

UCI Machine Learning Repository — [Online Retail Dataset](https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx)

---

## Licence

MIT
