# Projet : Scripts de manipulation d'une base de données SQLite

## Contexte
Ce dépôt contient des scripts Python réalisés dans le cadre d'un exercice de manipulation d'une base de données SQLite. Ces scripts visent à développer des compétences en création, manipulation et interrogation de bases de données relationnelles. Le projet couvre la création d'une base de données, des tables ainsi que l'insertion et la manipulation de données.

## Prérequis
- Connaissances de base du langage SQL
- IDE (Visual Studio Code, PyCharm, etc.)
- Installation de Python

## Installation

### 1. Installation de SQLite

- Télécharger SQLite depuis le [site officiel](https://sqlite.org/download.html) et suivre les instructions d'installation pour votre système d'exploitation (Windows ou Mac).
- Pour un environnement VSCode ou PyCharm, installer l'extension SQLite ou configurer SQLite via le terminal.

Pour vérifier l'installation, exécutez la commande suivante dans le terminal :
```bash
sqlite3 --version
```

## Scripts disponibles

### 1. Création de la base de données et des tables (`etape2.py`)
- Ce script permet de lancer SQLite et de créer deux tables dans la base de données :
  - **Clients** :
    - `id` (PRIMARY KEY)
    - `nom`
    - `prenom`
    - `email`
    - `date_inscription`
  - **Commandes** :
    - `id` (PRIMARY KEY)
    - `client_id` (FOREIGN KEY référencant l'id de la table Clients)
    - `produit`
    - `date_commande`

### 2. Insertion des données (`etape3.py`)
- Ce script insère des données dans les tables **Clients** et **Commandes**.
- Cinq clients et 10 commandes sont ajoutés à la base de données.

### 3. Manipulation des données et requêtes
- Ce script permet d'effectuer diverses opérations sur la base de données :
  - **Sélectionner tous les clients** (`etape4A.py`)
  - **Récupérer les commandes d'un client spécifique** (`etape4B.py`)
  - **Mettre à jour l'adresse e-mail d'un client** (`etape4C.py`)
  - **Supprimer une commande** (`etape4D.py`)

### 4. Sauvegarde et export des données (`etape5.py`)
- Ce script permet de sauvegarder la base de données et d'exporter les données des tables vers un fichier CSV pour une analyse externe.

## Utilisation
Pour exécuter les scripts, suivez les étapes suivantes :
1. Clonez ce repository sur votre machine locale.
2. Installez SQLite (si ce n'est pas déjà fait).
3. Exécutez les scripts Python dans l'ordre suivant :
   - `etape2.py` : pour créer la base de données et les tables.
   - `etape3.py` : pour insérer les données dans les tables.
   - `etape4A.py` : pour sélectionner tous les clients.
   - `etape4B.py` : pour récupérer les commandes d'un client spécifique.
   - `etape4C.py` : pour mettre à jour l'adresse e-mail d'un client.
   - `etape4D.py` : pour supprimer une commande.
   - `etape5.py` : pour sauvegarder et exporter les données.

N'oubliez pas d'utiliser [SQLite Viewer](https://sqliteviewer.com/) si vous avez besoin de visualiser la base facilement.