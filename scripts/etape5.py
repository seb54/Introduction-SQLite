import sqlite3
import csv
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

def exporter_donnees_jointure(conn, output_csv_path):
    """
    Effectue une jointure des tables Clients et Commandes et exporte les données dans un fichier CSV.
    
    Paramètres :
    conn (sqlite3.Connection) : Objet de connexion à la base de données SQLite.
    output_csv_path (str) : Le chemin vers le fichier CSV de sortie.
    """
    cursor = conn.cursor()
    try:
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
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            # Écrire l'en-tête
            writer.writerow([
                'client_id', 'nom', 'prenom', 'email', 'date_inscription',
                'commande_id', 'produit', 'date_commande'
            ])
            # Écrire les données
            writer.writerows(data)

        logging.info("Les données des tables 'Clients' et 'Commandes' ont été exportées avec succès dans '%s'.", output_csv_path)
    except sqlite3.Error as e:
        logging.error(f"Échec de la récupération des données : {e}")
        raise RuntimeError(f"Échec de la récupération des données : {e}")
    except OSError as e:
        logging.error(f"Erreur lors de l'écriture du fichier CSV : {e}")
        raise RuntimeError(f"Erreur lors de l'écriture du fichier CSV : {e}")
    finally:
        cursor.close()

def main():
    """
    Fonction principale pour gérer la connexion à la base de données et l'exportation des données jointes.
    """
    db_path = '../bdd/db.sqlite'
    output_csv_path = '../csv/clients_commandes.csv'
    
    try:
        # Se connecter à la base de données
        with connect_to_database(db_path) as conn:
            exporter_donnees_jointure(conn, output_csv_path)
    except (ConnectionError, RuntimeError) as e:
        logging.error(f"Erreur : {e}")
    except Exception as e:
        logging.critical(f"Une erreur inattendue est survenue : {e}")

if __name__ == "__main__":
    main()