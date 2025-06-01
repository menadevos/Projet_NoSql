# cassandra_connexion.py
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import threading

class CassandraConnection:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(CassandraConnection, cls).__new__(cls)
                    cls._instance._init_connection()
        return cls._instance

    def _init_connection(self):
        try:
            self.cluster = Cluster(['127.0.0.1'])
            self.session = self.cluster.connect()
            self._create_keyspace_and_tables()
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

def get_session():
    try:
        connection = CassandraConnection()
        session = connection.get_session()
        if session is None:
            raise Exception("Cassandra session is not initialized")
        return session
    except Exception as e:
        raise Exception(f"Erreur lors de la connexion à Cassandra: {str(e)}")