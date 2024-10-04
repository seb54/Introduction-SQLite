import sqlite3
import locale
from datetime import datetime

# Définir la locale en français
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Connexion à la base de données
conn = sqlite3.connect('../bdd/db.sqlite')

# Création d'un curseur pour interagir avec la base de données
cursor = conn.cursor()

# Demander l'ID du client pour lequel on souhaite récupérer les commandes
client_id = int(input("Entrez l'ID du client : "))

# Sélectionner toutes les commandes pour ce client spécifique
cursor.execute('''
    SELECT Commandes.id, Commandes.produit, Commandes.date_commande
    FROM Commandes
    WHERE Commandes.client_id = ?
''', (client_id,))

# Récupérer toutes les lignes (toutes les commandes du client)
commandes = cursor.fetchall()

# Vérifier si des commandes existent pour ce client
if commandes:
    print(f"Commandes pour le client ID {client_id} :")
    for commande in commandes:
        # Conversion de la date au format datetime (en supposant que commande[2] est une chaîne de caractères au format 'YYYY-MM-DD')
        date_commande = datetime.strptime(commande[2], '%Y-%m-%d')

        # Formater la date en français
        date_commande_fr = date_commande.strftime('%A %d %B %Y')
        
        print(f"ID Commande: {commande[0]}, Produit: {commande[1]}, Date: {date_commande_fr}")
else:
    print(f"Aucune commande trouvée pour le client ID {client_id}.")

# Fermeture de la connexion
conn.close()
