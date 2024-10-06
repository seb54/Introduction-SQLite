import sqlite3
import os
import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def connect_to_database(db_path):
    """
    Établit une connexion à la base de données SQLite.
    
    Paramètres :
    db_path (str) : Le chemin vers le fichier de la base de données SQLite.
    
    Retourne :
    sqlite3.Connection : Objet de connexion à la base de données SQLite.
    """
    if not os.path.exists(os.path.dirname(db_path)):
        os.makedirs(os.path.dirname(db_path))
    try:
        conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        logging.info("Connexion à la base de données établie avec succès.")
        return conn
    except sqlite3.Error as e:
        raise ConnectionError(f"Échec de la connexion à la base de données : {e}")

def verifier_email(email):
    """
    Vérifie si l'adresse e-mail a un format valide.
    
    Paramètres :
    email (str) : L'adresse e-mail à vérifier.
    
    Retourne :
    bool : True si l'email est valide, False sinon.
    """
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def verifier_client_id(client_id):
    """
    Vérifie si l'ID du client est un entier positif.
    
    Paramètres :
    client_id (int) : L'ID du client à vérifier.
    
    Retourne :
    bool : True si l'ID est valide, False sinon.
    """
    return isinstance(client_id, int) and client_id > 0

def mettre_a_jour_email_client(conn, client_id, nouvel_email):
    """
    Met à jour l'adresse e-mail d'un client spécifique.
    
    Paramètres :
    conn (sqlite3.Connection) : Objet de connexion à la base de données SQLite.
    client_id (int) : L'ID du client dont l'email doit être mis à jour.
    nouvel_email (str) : La nouvelle adresse e-mail du client.
    """
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE Clients
            SET email = ?
            WHERE id = ?
        ''', (nouvel_email, client_id))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"L'email du client ID {client_id} a été mis à jour avec succès.")
        else:
            print(f"Aucun client trouvé avec l'ID {client_id}.")
    except sqlite3.Error as e:
        raise RuntimeError(f"Échec de la mise à jour de l'email : {e}")
    finally:
        cursor.close()

def main():
    """
    Fonction principale pour gérer la connexion à la base de données et la mise à jour de l'email d'un client spécifique.
    """
    db_path = '../bdd/db.sqlite'
    
    try:
        # Se connecter à la base de données
        with connect_to_database(db_path) as conn:
            while True:
                client_id = input("Entrez l'ID du client dont vous souhaitez mettre à jour l'email : ")
                if client_id.isdigit() and int(client_id) > 0:
                    client_id = int(client_id)
                    break
                else:
                    print("L'ID du client doit être un entier positif. Veuillez réessayer.")

            while True:
                nouvel_email = input("Entrez la nouvelle adresse e-mail : ")
                if verifier_email(nouvel_email):
                    break
                else:
                    print("L'adresse e-mail fournie n'est pas valide. Veuillez réessayer.")

            mettre_a_jour_email_client(conn, client_id, nouvel_email)
    except (ConnectionError, RuntimeError) as e:
        logging.error(f"Erreur : {e}")
    except Exception as e:
        logging.critical(f"Une erreur inattendue est survenue : {e}")

if __name__ == "__main__":
    main()