# -*- coding: utf-8 -*-
# cassandra_connexion.py

from cassandra.cluster import Cluster

def get_session():
    cluster = Cluster(['127.0.0.1'])  # adresse locale
    session = cluster.connect('gestion_etudiants')  # le keyspace que j'ai  déjà créé
    return session
