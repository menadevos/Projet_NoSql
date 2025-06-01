from cassandra_connexion import get_session
import uuid

# On récupère la session une seule fois (optimisation)
session = get_session()

def ajouter_cours(nom, enseignant):
    id_cours = uuid.uuid4()
    query = """
        INSERT INTO cours (id, nom, enseignant)
        VALUES (%s, %s, %s)
    """
    session.execute(query, (id_cours, nom, enseignant))
    return id_cours

def lister_cours():
    query = "SELECT id, nom, enseignant FROM cours"
    rows = session.execute(query)
    return list(rows)
