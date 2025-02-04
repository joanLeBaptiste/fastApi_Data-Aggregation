# Projet Analyse de la Qualité de Vie des Personnes Âgées à Angers

## Description du projet
Ce projet a été réalisé par JoanLeBaptiste. Le but de ce projet est d'analyser la **qualité de vie des personnes âgées** à Angers en utilisant différentes données géographiques et des infrastructures locales.

Le projet est conçu sous forme d'une API FastAPI qui génère des graphiques. Les utilisateurs peuvent accéder à plusieurs visualisations via des liens locaux.

## Installation

#### Prérequis:
- Python >= 3.8

### 1. Téléchargez les dépendances du projet

Creez un environnement virtuel
```
python -m venv venv
source venv/bin/activate  # sur macOS/Linux
venv\Scripts\activate     # sur Windows
```
Dans le terminal, exécutez la commande suivante pour installer les dépendances:

```
pip install -r requirements.txt
```
### 2. **Créer une nouvelle base de données dans MySQL**  
   - Ouvrez **MySQL Workbench** ou un autre client MySQL.
   - Exécutez le script SQL fourni pour créer la base et insérer les données :
```
mysql -u root -p < database/script_Database.sql
```
Nous utilisons un fichier `.env` pour stocker les informations de connexion.
Copiez le fichier `.env.example` et renommez-le en `.env`
```
cp .env.example .env
```
### 3. **Modifiez `.env` avec vos propres identifiants MySQL**  
   Exemple :
```
DATABASE_URL=mysql+mysqlconnector://root:motdepasse@127.0.0.1:3306/fastapi_project
```
Lancez le projet:
```
uvicorn app.main:app --reload
```
### 4. **Le projet charge automatiquement cette configuration grâce à `config.py`** 

## Accéder aux pages disponibles
1. **Heatmap densité infrasctructures**  
   [http://127.0.0.1:8000/heatmap](http://127.0.0.1:8000/heatmap)

2. **Heatmap distances aux infrastructures**  
   [http://127.0.0.1:8000/superheatmap](http://127.0.0.1:8000/superheatmap)

3. **Affichage des centres zones avec chemins**  
   [http://127.0.0.1:8000/chemins](http://127.0.0.1:8000/chemins)

4. **Carte des zones**  
   [http://127.0.0.1:8000/map](http://127.0.0.1:8000/map)

5. **Scores des zones, graphique**  
   [http://127.0.0.1:8000/zones](http://127.0.0.1:8000/zones)
6. **Score attribué aux infrastructures**

   [http://127.0.0.1:8000/test](http://127.0.0.1:8000/test)_
