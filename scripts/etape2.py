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
        logging.error(f"Échec de la connexion à la base de données : {e}")
        raise ConnectionError(f"Échec de la connexion à la base de données : {e}")

def creer_tables(conn):
    """
    Crée les tables Clients et Commandes dans la base de données si elles n'existent pas déjà.
    
    Paramètres :
    conn (sqlite3.Connection) : Objet de connexion à la base de données SQLite.
    """
    cursor = conn.cursor()
    try:
        # Création de la table Clients
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                email TEXT NOT NULL,
                date_inscription DATE NOT NULL
            )
        ''')
        logging.info("Table 'Clients' créée ou déjà existante.")

        # Création de la table Commandes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Commandes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                produit TEXT NOT NULL,
                date_commande DATE NOT NULL,
                FOREIGN KEY (client_id) REFERENCES Clients(id)
            )
        ''')
        logging.info("Table 'Commandes' créée ou déjà existante.")
    except sqlite3.Error as e:
        logging.error(f"Échec de la création des tables : {e}")
        raise RuntimeError(f"Échec de la création des tables : {e}")
    finally:
        cursor.close()

def main():
    """
    Fonction principale pour gérer la connexion à la base de données et la création des tables.
    """
    db_path = '../bdd/db.sqlite'
    
    try:
        # Se connecter à la base de données
        with connect_to_database(db_path) as conn:
            creer_tables(conn)
    except (ConnectionError, RuntimeError) as e:
        logging.error(f"Erreur : {e}")
    except Exception as e:
        logging.critical(f"Une erreur inattendue est survenue : {e}")

if __name__ == "__main__":
    main()