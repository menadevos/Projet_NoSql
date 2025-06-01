# services.py

from statiques import get_session, get_statistiques_validation, get_best_note_by_cours, get_notes_by_etudiant, calcul_moyenne_notes_etudiant
import matplotlib.pyplot as plt

session = get_session()

def get_all_etudiants():
    etudiants = session.execute("SELECT id, nom, prenom FROM etudiants")
    return {f"{e['prenom']} {e['nom']}": e['id'] for e in etudiants}

def get_all_cours():
    cours = session.execute("SELECT id, nom FROM cours")
    return {c['nom']: c['id'] for c in cours}

def generate_graph_for_cours(cours_id):
    stats = get_statistiques_validation(cours_id)
    meilleure_note = get_best_note_by_cours(cours_id)

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(
        [stats["valides"], stats["rattrapages"], stats["non_valides"]],
        labels=["Validés", "Rattrapage", "Non validés"],
        autopct="%1.1f%%",
        colors=["#4CAF50", "#FFC107", "#F44336"]
    )
    ax.set_title("Statistiques de Validation")

    return fig, meilleure_note

def generate_graph_for_etudiant(etudiant_id):
    notes = get_notes_by_etudiant(etudiant_id)
    cours_notes = [
        (session.execute("SELECT nom FROM cours WHERE id=%s", (n["cours_id"],)).one()["nom"], n["note"])
        for n in notes
    ]
    cours_notes.sort(key=lambda x: x[1], reverse=True)

    if not cours_notes:
        return None, 0

    noms, notes = zip(*cours_notes)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(noms, notes, color="#2196F3")
    ax.set_ylabel("Note")
    ax.set_xlabel("Cours")
    ax.set_title("Notes par Cours")
    ax.set_ylim(0, 20)
    plt.xticks(rotation=45)

    moyenne = calcul_moyenne_notes_etudiant(etudiant_id)

    return fig, moyenne
