from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

# Création du keyspace
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS gestion_etudiants
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
""")

session.set_keyspace('gestion_etudiants')

# Table étudiants
session.execute("""
    CREATE TABLE IF NOT EXISTS etudiants (
        id UUID PRIMARY KEY,
        nom TEXT,
        prenom TEXT,
        email TEXT,
        date_naissance DATE
    )
""")

# Table cours
session.execute("""
    CREATE TABLE IF NOT EXISTS cours (
        id UUID PRIMARY KEY,
        nom TEXT,
        enseignant TEXT
    )
""")

# Table notes
session.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        etudiant_id UUID,
        cours_id UUID,
        annee TEXT,
        note FLOAT,
        PRIMARY KEY ((etudiant_id), cours_id)
    )
""")

print("✅ Keyspace et tables créés avec succès.")
 
