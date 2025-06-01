# 
from uuid import uuid1
from cassandra_connexion import CassandraConnection


class CoursService:
    def __init__(self ,session):
        self.session = CassandraConnection().get_session()

    def ajouter_cours(self, nom, enseignant):
        if not self.session:
            raise Exception("Pas de session Cassandra disponible")
        new_id = uuid1()
        self.session.execute(
            "INSERT INTO cours (id, nom, enseignant) VALUES (%s, %s, %s)",
            (new_id, nom, enseignant)
        )

    def get_all_cours(self):
        if not self.session:
            raise Exception("Pas de session Cassandra disponible")
        rows = self.session.execute("SELECT id, nom, enseignant FROM cours")
        return list(rows)
