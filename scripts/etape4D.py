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

def supprimer_commande(conn, commande_id):
    """
    Supprime une commande spécifique de la base de données.
    
    Paramètres :
    conn (sqlite3.Connection) : Objet de connexion à la base de données SQLite.
    commande_id (int) : L'ID de la commande à supprimer.
    """
    cursor = conn.cursor()
    try:
        cursor.execute('''
            DELETE FROM Commandes
            WHERE id = ?
        ''', (commande_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"La commande ID {commande_id} a été supprimée avec succès.")
            return True
        else:
            print(f"Aucune commande trouvée avec l'ID {commande_id}. Veuillez réessayer.")
            return False
    except sqlite3.Error as e:
        raise RuntimeError(f"Échec de la suppression de la commande : {e}")
    finally:
        cursor.close()

def main():
    """
    Fonction principale pour gérer la connexion à la base de données et la suppression d'une commande spécifique.
    """
    db_path = '../bdd/db.sqlite'
    
    try:
        # Se connecter à la base de données
        with connect_to_database(db_path) as conn:
            while True:
                commande_id = input("Entrez l'ID de la commande que vous souhaitez supprimer : ")
                if commande_id.isdigit() and int(commande_id) > 0:
                    commande_id = int(commande_id)
                    if supprimer_commande(conn, commande_id):
                        break
                else:
                    print("L'ID de la commande doit être un entier positif. Veuillez réessayer.")
    except (ConnectionError, RuntimeError) as e:
        logging.error(f"Erreur : {e}")
    except Exception as e:
        logging.critical(f"Une erreur inattendue est survenue : {e}")

if __name__ == "__main__":
    main()