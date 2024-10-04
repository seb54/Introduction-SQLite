import sqlite3

# Connexion à la base de données (le fichier sera créé s'il n'existe pas)
conn = sqlite3.connect('../bdd/db.sqlite')

# Création d'un curseur pour interagir avec la base de données
cursor = conn.cursor()

# Création de la table Clients
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        email TEXT NOT NULL,
        date_inscription DATE
    )
''')

# Création de la table Commandes avec clé étrangère client_id
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Commandes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        produit TEXT NOT NULL,
        date_commande DATE,
        FOREIGN KEY (client_id) REFERENCES Clients(id)
    )
''')

# Enregistrement des changements
conn.commit()

# Fermeture de la connexion
conn.close()

print("Tables 'Clients' et 'Commandes' créées avec succès.")
