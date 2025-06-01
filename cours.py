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



def update_cours(id_cours, nom=None, enseignant=None):
    # On construit la requête dynamiquement selon les champs à mettre à jour
    updates = []
    params = []

    if nom is not None:
        updates.append("nom = %s")
        params.append(nom)

    if enseignant is not None:
        updates.append("enseignant = %s")
        params.append(enseignant)

    if not updates:
        # Rien à mettre à jour
        return False

    params.append(id_cours)  # pour la clause WHERE

    query = f"""
        UPDATE cours
        SET {', '.join(updates)}
        WHERE id = %s
    """
    session.execute(query, tuple(params))
    return True
