from cassandra_connexion import get_session
import uuid

def ajouter_cours(nom, enseignant):
    session = get_session()
    id_cours = uuid.uuid4()
    session.execute("""
        INSERT INTO cours (id, nom, enseignant)
        VALUES (%s, %s, %s)
    """, (id_cours, nom, enseignant))
    return id_cours

def lister_cours():
    session = get_session()
    rows = session.execute("SELECT id, nom, enseignant FROM cours")
    return list(rows)
