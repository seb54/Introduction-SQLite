import sqlite3
import re

# Connexion à la base de données
conn = sqlite3.connect('../bdd/db.sqlite')

# Création d'un curseur pour interagir avec la base de données
cursor = conn.cursor()

# Demander l'ID du client pour lequel on souhaite mettre à jour l'email
client_id = int(input("Entrez l'ID du client dont vous souhaitez mettre à jour l'email : "))

# Demander la nouvelle adresse e-mail
nouveau_email = input("Entrez la nouvelle adresse e-mail : ")

# Vérification de la validité de l'adresse e-mail
def verifier_email(email):
    # Regex pour valider une adresse email
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(regex, email):
        return True
    else:
        return False

# Vérifier si l'adresse e-mail est valide
if verifier_email(nouveau_email):
    # Mettre à jour l'adresse e-mail du client dans la base de données
    cursor.execute('''
        UPDATE Clients
        SET email = ?
        WHERE id = ?
    ''', (nouveau_email, client_id))

    # Vérifier si la mise à jour a bien été effectuée
    if cursor.rowcount > 0:
        print(f"L'adresse e-mail du client ID {client_id} a été mise à jour avec succès.")
    else:
        print(f"Aucun client trouvé avec l'ID {client_id}.")
else:
    print("L'adresse e-mail saisie est invalide. Veuillez entrer une adresse e-mail correcte.")

# Enregistrer les changements
conn.commit()

# Fermeture de la connexion
conn.close()
