import sqlite3
import os
import logging
from datetime import date, datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Définir une fonction de conversion pour les dates
def adapt_date(dt):
    return dt.strftime('%Y-%m-%d')

def convert_date(s):
    return datetime.strptime(s.decode(), '%Y-%m-%d')

# Enregistrer les adaptateurs et convertisseurs pour sqlite3
sqlite3.register_adapter(date, adapt_date)
sqlite3.register_adapter(datetime, adapt_date)
sqlite3.register_converter("date", convert_date)

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
        # Ajoutez detect_types=sqlite3.PARSE_DECLTYPES pour détecter les types enregistrés
        conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        logging.info("Connexion à la base de données établie avec succès.")
        return conn
    except sqlite3.Error as e:
        raise ConnectionError(f"Échec de la connexion à la base de données : {e}")

def afficher_clients(conn):
    """
    Affiche les informations des clients.
    
    Paramètres :
    conn (sqlite3.Connection) : Objet de connexion à la base de données SQLite.
    """
    cursor = conn.cursor()
    try:
        # Sélectionner tous les clients
        cursor.execute('SELECT * FROM Clients')
        clients = cursor.fetchall()
        
        # Afficher chaque client
        for client in clients:
            date_inscription = client[4] if isinstance(client[4], (date, datetime)) else None

            if date_inscription:
                # Formatter pour ne montrer que la partie date
                date_str = date_inscription.strftime('%Y-%m-%d')
                print(f"ID: {client[0]}, Nom: {client[1]}, Prénom: {client[2]}, Email: {client[3]}, Date d'inscription: {date_str}")
            else:
                print(f"ID: {client[0]}, Nom: {client[1]}, Prénom: {client[2]}, Email: {client[3]}, Date d'inscription: Non disponible")

    except sqlite3.Error as e:
        raise RuntimeError(f"Échec de la récupération des clients : {e}")
    finally:
        cursor.close()

def main():
    """
    Fonction principale pour gérer la connexion à la base de données et l'affichage des clients.
    """
    db_path = '../bdd/db.sqlite'
    
    try:
        # Se connecter à la base de données et afficher les clients
        with connect_to_database(db_path) as conn:
            afficher_clients(conn)
    except (ConnectionError, RuntimeError) as e:
        logging.error(f"Erreur : {e}")
    except Exception as e:
        logging.critical(f"Une erreur inattendue est survenue : {e}")

if __name__ == "__main__":
    main()
