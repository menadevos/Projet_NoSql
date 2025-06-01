from cassandra_connexion import get_session
import uuid

# Ajouter un etudiant
def ajouter_etudiant(nom, prenom, email, date_naissance):
    session = get_session()
    id_etudiant = uuid.uuid4()
    session.execute("""
        INSERT INTO etudiants (id, nom, prenom, email, date_naissance)
        VALUES (%s, %s, %s, %s, %s)
    """, (id_etudiant, nom, prenom, email, date_naissance))
    return id_etudiant

# Recuperer tous les etudiants
def lister_etudiants():
    session = get_session()
    rows = session.execute("SELECT id, nom, prenom, email, date_naissance FROM etudiants")
    return list(rows)

# Modifier un etudiant
def modifier_etudiant(id_etudiant, nom, prenom, email, date_naissance):
    session = get_session()
    session.execute("""
        UPDATE etudiants SET nom=%s, prenom=%s, email=%s, date_naissance=%s
        WHERE id=%s
    """, (nom, prenom, email, date_naissance, id_etudiant))

# Supprimer un etudiant
def supprimer_etudiant(id_etudiant):
    session = get_session()
    session.execute("DELETE FROM etudiants WHERE id=%s", (id_etudiant,))