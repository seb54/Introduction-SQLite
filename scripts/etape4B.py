import sqlite3
import os
import logging

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

def afficher_commandes_client(conn, client_id):
    """
    Affiche les commandes pour un client spécifique.
    
    Paramètres :
    conn (sqlite3.Connection) : Objet de connexion à la base de données SQLite.
    client_id (int) : L'ID du client pour lequel les commandes doivent être récupérées.
    """
    cursor = conn.cursor()
    try:
        # Sélectionner toutes les commandes pour ce client spécifique
        cursor.execute('''
            SELECT Commandes.id, Commandes.produit, Commandes.date_commande
            FROM Commandes
            WHERE Commandes.client_id = ?
        ''', (client_id,))

        commandes = cursor.fetchall()

        # Vérifier si des commandes existent pour ce client
        if commandes:
            print(f"Commandes pour le client ID {client_id} :")
            for commande in commandes:
                print(f"ID Commande: {commande[0]}, Produit: {commande[1]}, Date: {commande[2]}")
        else:
            print(f"Aucune commande trouvée pour le client ID {client_id}.")
    except sqlite3.Error as e:
        raise RuntimeError(f"Échec de la récupération des commandes : {e}")
    finally:
        cursor.close()

def main():
    """
    Fonction principale pour gérer la connexion à la base de données et l'affichage des commandes pour un client spécifique.
    """
    db_path = '../bdd/db.sqlite'
    
    try:
        # Se connecter à la base de données
        with connect_to_database(db_path) as conn:
            client_id = int(input("Entrez l'ID du client pour lequel vous souhaitez récupérer les commandes : "))
            afficher_commandes_client(conn, client_id)
    except (ConnectionError, RuntimeError) as e:
        logging.error(f"Erreur : {e}")
    except Exception as e:
        logging.critical(f"Une erreur inattendue est survenue : {e}")

if __name__ == "__main__":
    main()
