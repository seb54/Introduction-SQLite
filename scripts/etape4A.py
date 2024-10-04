import sqlite3
import locale
from datetime import datetime

# Définir la locale en français
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Connexion à la base de données
conn = sqlite3.connect('../bdd/db.sqlite')

# Création d'un curseur pour interagir avec la base de données
cursor = conn.cursor()

# Sélectionner tous les clients
cursor.execute('SELECT * FROM Clients')

# Récupérer toutes les lignes (tous les clients)
clients = cursor.fetchall()

# Afficher chaque client
for client in clients:
    # Conversion de la date au format datetime (en supposant que client[4] est une chaîne de caractères au format 'YYYY-MM-DD')
    date_inscription = datetime.strptime(client[4], '%Y-%m-%d')
    
    # Formater la date en français
    date_inscription_fr = date_inscription.strftime('%A %d %B %Y')
    
    print(f"ID: {client[0]}, Nom: {client[1]}, Prénom: {client[2]}, Email: {client[3]}, Date d'inscription: {date_inscription_fr}")

# Fermeture de la connexion
conn.close()
