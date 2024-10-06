import sqlite3
import os
import logging
from datetime import date, datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Adaptateurs pour convertir les objets date en texte (et inversement)
def adapt_date(iso_date):
    return iso_date.isoformat()

def convert_date(iso_str):
    return date.fromisoformat(iso_str)

# Enregistrer les adaptateurs dans SQLite
sqlite3.register_adapter(date, adapt_date)
sqlite3.register_converter("DATE", convert_date)

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

def insert_clients_and_orders(conn):
    """
    Insère des données dans les tables Clients et Commandes.
    
    Paramètres :
    conn (sqlite3.Connection) : Objet de connexion à la base de données SQLite.
    """
    cursor = conn.cursor()
    try:
        # Insertion de clients dans la table Clients (personnages des Simpsons)
        clients = [
            ('Simpson', 'Homer', 'homer.simpson@springfield.com', date(2023, 10, 1)),
            ('Simpson', 'Marge', 'marge.simpson@springfield.com', date(2023, 10, 2)),
            ('Simpson', 'Bart', 'bart.simpson@springfield.com', date(2023, 10, 3)),
            ('Simpson', 'Lisa', 'lisa.simpson@springfield.com', date(2023, 10, 4)),
            ('Simpson', 'Maggie', 'maggie.simpson@springfield.com', date(2023, 10, 5))
        ]
        cursor.executemany('''
            INSERT INTO Clients (nom, prenom, email, date_inscription)
            VALUES (?, ?, ?, ?)
        ''', clients)
        logging.info("Données insérées dans la table 'Clients'.")
        
        # Récupérer les ids des clients pour les utiliser dans les commandes
        cursor.execute('SELECT id FROM Clients WHERE email = "homer.simpson@springfield.com"')
        client_homer_id = cursor.fetchone()[0]
        
        cursor.execute('SELECT id FROM Clients WHERE email = "marge.simpson@springfield.com"')
        client_marge_id = cursor.fetchone()[0]
        
        cursor.execute('SELECT id FROM Clients WHERE email = "bart.simpson@springfield.com"')
        client_bart_id = cursor.fetchone()[0]
        
        cursor.execute('SELECT id FROM Clients WHERE email = "lisa.simpson@springfield.com"')
        client_lisa_id = cursor.fetchone()[0]
        
        cursor.execute('SELECT id FROM Clients WHERE email = "maggie.simpson@springfield.com"')
        client_maggie_id = cursor.fetchone()[0]
        
        # Insertion de dix commandes dans la table Commandes
        commandes = [
            (client_homer_id, 'Duff Beer', date(2023, 10, 6)),
            (client_marge_id, 'Vacuum Cleaner', date(2023, 10, 7)),
            (client_bart_id, 'Skateboard', date(2023, 10, 8)),
            (client_lisa_id, 'Saxophone Reeds', date(2023, 10, 9)),
            (client_maggie_id, 'Pacifier', date(2023, 10, 10)),
            (client_homer_id, 'Donuts', date(2023, 10, 11)),
            (client_marge_id, 'Groceries', date(2023, 10, 12)),
            (client_bart_id, 'Slingshot', date(2023, 10, 13)),
            (client_lisa_id, 'Jazz Records', date(2023, 10, 14)),
            (client_maggie_id, 'Stuffed Animal', date(2023, 10, 15))
        ]
        cursor.executemany('''
            INSERT INTO Commandes (client_id, produit, date_commande)
            VALUES (?, ?, ?)
        ''', commandes)
        logging.info("Données insérées dans la table 'Commandes'.")
    except sqlite3.Error as e:
        raise RuntimeError(f"Échec de l'insertion des données : {e}")

def main():
    """
    Fonction principale pour gérer l'insertion des données dans la base de données.
    """
    db_path = '../bdd/db.sqlite'
    
    try:
        # Étape 1 : Se connecter à la base de données
        with connect_to_database(db_path) as conn:
            # Étape 2 : Insérer des données dans les tables Clients et Commandes
            insert_clients_and_orders(conn)
            
            # Étape 3 : Enregistrer les changements
            conn.commit()
            logging.info("Données insérées dans les tables 'Clients' et 'Commandes' avec succès.")
            print("Données insérées dans les tables 'Clients' et 'Commandes' avec succès.")
    except (ConnectionError, RuntimeError) as e:
        logging.error(f"Erreur : {e}")
        print(f"Erreur : {e}")
    except Exception as e:
        logging.critical(f"Une erreur inattendue est survenue : {e}")
        print(f"Une erreur inattendue est survenue : {e}")

if __name__ == "__main__":
    main()
