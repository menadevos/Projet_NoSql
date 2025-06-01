# cassandra_connexion.py
# database.py
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement#Pour exécuter des requêtes CQL simple
import threading


class CassandraConnection:
    _instance = None #pattern Singleton
    _lock = threading.Lock() # Pour assurer la sécurité des threads

    def __new__(cls): #cls = la classe elle-même
        if not cls._instance: # Vérifie si une instance existe déjà
            with cls._lock:  # Assure que la création de l'instance est thread-safe
                if not cls._instance:
                    cls._instance = super(CassandraConnection, cls).__new__(cls)
                    cls._instance._init_connection()
        return cls._instance

    def _init_connection(self):
        try:
            self.cluster = Cluster(['127.0.0.1'])
             # Créer d'abord la session sans keyspace spécifique
            self.session = self.cluster.connect()
        
        # Maintenant qu'on a une session, créer le keyspace et les tables
            self._create_keyspace_and_tables()
        
        # Se connecter au keyspace après sa création
            self.session.set_keyspace('gestion_etudiants')
            
        except Exception as e:
            print(f"[Erreur Cassandra] {e}")
            self.cluster = None
            self.session = None

    def _create_keyspace_and_tables(self):
        self.session.execute("""
            CREATE KEYSPACE IF NOT EXISTS gestion_etudiants 
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
        """)
        self.session.set_keyspace('gestion_etudiants')

        self.session.execute("""
            CREATE TABLE IF NOT EXISTS etudiants (
                id UUID PRIMARY KEY,
                nom TEXT,
                prenom TEXT,
                email TEXT,
                date_naissance DATE
            )
        """)
        self.session.execute("""
            CREATE TABLE IF NOT EXISTS cours (
                id UUID PRIMARY KEY,
                nom TEXT,
                enseignant TEXT
            )
        """)
        self.session.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                etudiant_id UUID,
                cours_id UUID,
                annee INT,
                note FLOAT,
                PRIMARY KEY (etudiant_id, cours_id, annee)
            )
        """)

    def get_session(self):
        return self.session
