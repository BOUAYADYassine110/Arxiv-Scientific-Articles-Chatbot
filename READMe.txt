# ArXiv Research Hub

**ArXiv Research Hub** est un chatbot de recherche scientifique permettant d'explorer plus de 4 000 publications arXiv via une interface web moderne et deux modes de recherche (manuelle et sémantique).

---

## 🚀 Fonctionnalités

* **Recherche Manuelle** : filtrage SQL + similarité vectorielle FAISS
* **Recherche AI (sémantique)** : extraction automatique de paramètres via LLM + FAISS
* **Interface Web** : développée avec Streamlit, support thème clair/sombre
* **Visualisations** : graphiques publications/année et répartition catégories
* **Indexation** : génération d'embeddings avec Sentence-Transformers et FAISS
* **Stockage** : base SQLite relationnelle (articles, authors, article\_authors)

## 🧩 Architecture du projet

1. **extract\_data.py**

   * Interroge l'API arXiv, collecte métadonnées (ID, titre, abstract, date, DOI, auteurs, catégories)
   * Génère `arxiv_data_raw.csv`

2. **clean\_and\_store.py**

   * Nettoiement (suppression doublons, formatage)
   * Conversion des catégories via `category_map`
   * Création & peuplement de `arxiv_data.db`

3. **index\_abstracts.py**

   * Lecture des abstracts depuis SQLite
   * Génération d'embeddings (`all-MiniLM-L6-v2`)
   * Construction d'un index FAISS et sauvegarde (`faiss_index.index`, `article_ids.csv`)

4. **connect\_llm.py**

   * Classe `LLMConnect` pour interroger un LLM cloud (Together API)
   * Extraction automatique de paramètres de recherche et explications

5. **chatbot.py**

   * Interface Streamlit
   * Chargement des ressources (index, IDs, modèle)
   * Zones de recherche & filtres avancés
   * Intégration des deux modes de recherche
   * Affichage des résultats et des graphiques

## 💻 Prérequis

* Python ≥ 3.8
* Virtualenv ou conda

Bibliothèques (à installer via `requirements.txt`) :

```text
pandas
numpy
streamlit
sentence-transformers
faiss-cpu
plotly
sqlite3  # inclus dans la stdlib
requests
arxiv
logging
```

## 📥 Installation



1. Créer un environnement virtuel :  
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate

2. Installer les dépendances :

pip install -r requirements.txt

## ▶️ Utilisation

1. **Extraction des données** :  

python extract_data.py

2. **Nettoyage & stockage** :

python clean\_and\_store.py


3. **Indexation** :  

python index_abstracts.py

4. **Lancer le chatbot** :

streamlit run chatbot.py

Ouvrir ensuite `http://localhost:8501` dans votre navigateur.

