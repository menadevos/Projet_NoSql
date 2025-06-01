# etudiants.py
from cassandra_connexion import get_session
from uuid import UUID, uuid4
from datetime import date
from typing import List, Tuple
from cassandra.query import SimpleStatement
import re


def validate_email(email: str) -> bool:
    """
    Valide le format de l'adresse email.

    Args:
        email (str): Adresse email à valider

    Returns:
        bool: True si l'email est valide, False sinon
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))

def ajouter_etudiant(nom: str, prenom: str, email: str, date_naissance: date) -> UUID:
    """
    Ajoute un nouvel étudiant dans la table etudiants.

    Args:
        nom (str): Nom de l'étudiant
        prenom (str): Prénom de l'étudiant
        email (str): Adresse email de l'étudiant
        date_naissance (date): Date de naissance de l'étudiant

    Returns:
        UUID: ID de l'étudiant créé

    Raises:
        ValueError: Si les champs obligatoires sont vides ou si l'email est invalide
        Exception: En cas d'erreur lors de l'insertion dans la base de données
    """
    try:
        if not nom or not prenom or not email:
            raise ValueError("Nom, prénom et email sont obligatoires")
        if not validate_email(email):
            raise ValueError("Format d'email invalide")
        
        session = get_session()
        id_etudiant = uuid4()
        query = SimpleStatement("""
            INSERT INTO gestion_etudiants.etudiants (id, nom, prenom, email, date_naissance)
            VALUES (%s, %s, %s, %s, %s)
        """)
        session.execute(query, (id_etudiant, nom, prenom, email, date_naissance))
        return id_etudiant
    except Exception as e:
        raise Exception(f"Erreur lors de l'ajout de l'étudiant: {str(e)}")

def lister_etudiants() -> List[Tuple[UUID, str, str, str, date]]:
    """
    Récupère tous les étudiants de la table etudiants.

    Returns:
        List[Tuple[UUID, str, str, str, date]]: Liste des étudiants avec leurs informations

    Raises:
        Exception: En cas d'erreur lors de la récupération des données
    """
    try:
        session = get_session()
        query = SimpleStatement("SELECT id, nom, prenom, email, date_naissance FROM gestion_etudiants.etudiants")
        rows = session.execute(query)
        return list(rows)
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération des étudiants: {str(e)}")

def modifier_etudiant(id_etudiant: UUID, nom: str, prenom: str, email: str, date_naissance: date) -> None:
    """
    Modifie les informations d'un étudiant existant.

    Args:
        id_etudiant (UUID): ID de l'étudiant à modifier
        nom (str): Nouveau nom
        prenom (str): Nouveau prénom
        email (str): Nouvel email
        date_naissance (date): Nouvelle date de naissance

    Raises:
        ValueError: Si les champs obligatoires sont vides ou si l'email est invalide
        Exception: En cas d'erreur lors de la mise à jour
    """
    try:
        if not nom or not prenom or not email:
            raise ValueError("Nom, prénom et email sont obligatoires")
        if not validate_email(email):
            raise ValueError("Format d'email invalide")
        
        session = get_session()
        query = SimpleStatement("""
            UPDATE gestion_etudiants.etudiants SET nom=%s, prenom=%s, email=%s, date_naissance=%s
            WHERE id=%s
        """)
        session.execute(query, (nom, prenom, email, date_naissance, id_etudiant))
    except Exception as e:
        raise Exception(f"Erreur lors de la modification de l'étudiant: {str(e)}")

def supprimer_etudiant(id_etudiant: UUID) -> None:
    """
    Supprime un étudiant de la table etudiants.

    Args:
        id_etudiant (UUID): ID de l'étudiant à supprimer

    Raises:
        Exception: En cas d'erreur lors de la suppression
    """
    try:
        session = get_session()
        query = SimpleStatement("DELETE FROM gestion_etudiants.etudiants WHERE id=%s")
        session.execute(query, (id_etudiant,))
    except Exception as e:
        raise Exception(f"Erreur lors de la suppression de l'étudiant: {str(e)}")