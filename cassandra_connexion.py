# cassandra_connexion.py
from cassandra.cluster import Cluster
import threading

class CassandraConnection:  # Classe singleton pour gérer la connexion à Cassandra
    _instance = None # Singleton instance
    _lock = threading.Lock() # Thread-safe lock 


     #premiere metode qui sera appelée pour créer une instance
    def __new__(cls): #cls = class
        if not cls._instance: # si deja une instance exists
            with cls._lock: # pour s'assurer que l'instance est créée de manière thread-safe
                # Double-checked locking
                if not cls._instance:
                    cls._instance = super(CassandraConnection, cls).__new__(cls) #cree une instance de connection avec la classe parente ( object)
                    cls._instance._init_connection() # Appel de la méthode d'initialisation pour établir la connexion
        return cls._instance 

    # Initialisation de la connexion à Cassandra
    def _init_connection(self): #self = instance de la classe 
        try:
            self.cluster = Cluster(['127.0.0.1'])
             # Créer d'abord la session sans keyspace spécifique
            self.session = self.cluster.connect()
        
        # Maintenant qu'on a une session, créer le keyspace et les tables
            self._create_keyspace_and_tables()
        
        # Se connecter au keyspace après sa création
            self.session.set_keyspace('gestion_etudiants')
        except Exception as e: # Gérer les exceptions lors de la connexion
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



#fonction globale ( en dehors de classe ) pour obtenir la session Cassandra pour les autres fichiers qui importent ce module
def get_session():
    try:
        connection = CassandraConnection()
        session = connection.get_session()
        if session is None:
            raise Exception("Cassandra session is not initialized")
        return session
    except Exception as e:
        raise Exception(f"Erreur lors de la connexion à Cassandra: {str(e)}")