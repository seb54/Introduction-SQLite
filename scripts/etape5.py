import sqlite3
import csv

# Connexion à la base de données
conn = sqlite3.connect('../bdd/db.sqlite')

# Création d'un curseur pour interagir avec la base de données
cursor = conn.cursor()

# Jointure des tables Clients et Commandes
cursor.execute('''
    SELECT 
        Clients.id AS client_id, 
        Clients.nom, 
        Clients.prenom, 
        Clients.email, 
        Clients.date_inscription, 
        Commandes.id AS commande_id, 
        Commandes.produit, 
        Commandes.date_commande
    FROM Clients
    LEFT JOIN Commandes ON Clients.id = Commandes.client_id
''')

# Récupérer toutes les données après la jointure
data = cursor.fetchall()

# Exportation des données combinées dans un fichier CSV
with open('../csv/clients_commandes.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    # Écrire l'en-tête
    writer.writerow([
        'client_id', 'nom', 'prenom', 'email', 'date_inscription', 
        'commande_id', 'produit', 'date_commande'
    ])
    # Écrire les données
    writer.writerows(data)

print("Les données des tables 'Clients' et 'Commandes' ont été exportées avec succès dans 'clients_commandes.csv'.")

# Fermeture de la connexion
conn.close()
