# statiques.py

from cassandra_connexion import get_session

session = get_session()

def get_notes_by_cours(cours_id):
    query = "SELECT * FROM notes WHERE cours_id=%s ALLOW FILTERING"
    return session.execute(query, (cours_id,))

def get_notes_by_etudiant(etudiant_id):
    query = "SELECT * FROM notes WHERE etudiant_id=%s"
    return session.execute(query, (etudiant_id,))

def calcul_moyenne_notes_etudiant(etudiant_id):
    notes = get_notes_by_etudiant(etudiant_id)
    notes_list = [n["note"] for n in notes]
    return round(sum(notes_list) / len(notes_list), 2) if notes_list else 0

def calcul_moyenne_notes_cours(cours_id):
    notes = get_notes_by_cours(cours_id)
    notes_list = [n["note"] for n in notes]
    return round(sum(notes_list) / len(notes_list), 2) if notes_list else 0

def get_best_note_by_cours(cours_id):
    notes = get_notes_by_cours(cours_id)
    return max([n["note"] for n in notes], default=None)

def get_statistiques_validation(cours_id):
    notes = get_notes_by_cours(cours_id)
    valides = 0
    ratt = 0
    non_valides = 0
    for n in notes:
        if n["note"] >= 12:
            valides += 1
        elif n["note"] >= 8:
            ratt += 1
        else:
            non_valides += 1
    return {
        "valides": valides,
        "rattrapages": ratt,
        "non_valides": non_valides
    }
