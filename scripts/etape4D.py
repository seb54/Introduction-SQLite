import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('../bdd/db.sqlite')

# Création d'un curseur pour interagir avec la base de données
cursor = conn.cursor()

# Demander l'ID de la commande à supprimer
commande_id = int(input("Entrez l'ID de la commande à supprimer : "))

# Supprimer la commande de la base de données
cursor.execute('''
    DELETE FROM Commandes
    WHERE id = ?
''', (commande_id,))

# Vérifier si la suppression a bien été effectuée
if cursor.rowcount > 0:
    print(f"La commande ID {commande_id} a été supprimée avec succès.")
else:
    print(f"Aucune commande trouvée avec l'ID {commande_id}.")

# Enregistrer les changements
conn.commit()

# Fermeture de la connexion
conn.close()
