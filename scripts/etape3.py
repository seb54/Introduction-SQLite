import sqlite3
from datetime import date

# Adaptateurs pour convertir les objets date en texte (et inversement)
def adapt_date(iso_date):
    return iso_date.isoformat()

def convert_date(iso_str):
    return date.fromisoformat(iso_str)

# Enregistrer les adaptateurs dans SQLite
sqlite3.register_adapter(date, adapt_date)
sqlite3.register_converter("DATE", convert_date)

# Connexion à la base de données avec prise en charge du format DATE
conn = sqlite3.connect('../bdd/db.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)

# Création d'un curseur pour interagir avec la base de données
cursor = conn.cursor()

# Insertion de deux clients dans la table Clients
clients = [
    ('Dupont', 'Jean', 'jean.dupont@example.com', date(2023, 10, 1)),
    ('Martin', 'Marie', 'marie.martin@example.com', date(2023, 10, 2))
]
cursor.executemany('''
    INSERT INTO Clients (nom, prenom, email, date_inscription)
    VALUES (?, ?, ?, ?)
''', clients)

# Récupérer les ids des clients pour les utiliser dans les commandes
cursor.execute('SELECT id FROM Clients WHERE email = "jean.dupont@example.com"')
client_jean_id = cursor.fetchone()[0]

cursor.execute('SELECT id FROM Clients WHERE email = "marie.martin@example.com"')
client_marie_id = cursor.fetchone()[0]

# Insertion de deux commandes dans la table Commandes
commandes = [
    (client_jean_id, 'Laptop', date(2023, 10, 3)),
    (client_marie_id, 'Smartphone', date(2023, 10, 4))
]
cursor.executemany('''
    INSERT INTO Commandes (client_id, produit, date_commande)
    VALUES (?, ?, ?)
''', commandes)

# Enregistrement des changements
conn.commit()

# Fermeture de la connexion
conn.close()

print("Données insérées dans les tables 'Clients' et 'Commandes' avec succès.")
