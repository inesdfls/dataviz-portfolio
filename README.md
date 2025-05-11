# Portfolio DataViz & Health Analysis

**Application Streamlit** combinant un portfolio professionnel et une analyse interactive de données de santé publique françaises (pathologies et cancers).

## 🔍 Aperçu
- **Portfolio** : Présentation personnelle, compétences techniques (Python, SQL, etc.), et centres d'intérêt.
- **Analyse de données** : Exploration des pathologies en France (2015-2022) avec focus sur les cancers :
  - Répartition par âge, sexe, département.
  - Tendances temporelles et cartographie interactive (Heatmap + Choroplèthe).
  - Dataset source : [Data.gouv.fr](https://www.data.gouv.fr/fr/datasets/pathologies-effectif-de-patients-par-pathologie-sexe-classe-dage-et-territoire-departement-region/).

## 🛠️ Technologies
- **Frontend** : `Streamlit`
- **Visualisation** : `Altair` (graphiques), `Folium` (cartes), `PIL` (images).
- **Data** : `Pandas`, `GeoJSON`, caching avec `@st.cache_data`.

## 🚀 Fonctionnalités clés
1. **Onglets interactifs** :
   - *About Me* : CV dynamique avec visualisation des compétences.
   - *Health Data* : Filtres par année, département, type de pathologie.
2. **Carte géographique** :
   - Superposition de données de prévalence et de cas par département.
3. **Graphiques** :
   - Évolution temporelle, répartition par âge/sexe, analyse multi-niveaux (pathologies niv1-3).

## 📦 Installation
```bash
pip install streamlit pandas altair folium streamlit-folium requests pillow
streamlit run portfolio.py
