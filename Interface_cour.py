import tkinter as tk
from tkinter import ttk, messagebox
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from uuid import uuid1

class CourseManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Cours")
        self.root.geometry("500x320")
        self.root.configure(bg="#B3D9FF")

        # Connexion à Cassandra
        self.cluster = Cluster(['127.0.0.1'])  # Adapter à votre configuration
        self.session = self.cluster.connect()
        
        # Créer le keyspace et la table si inexistants
        self.setup_database()
        
        self.setup_ui()

    def setup_database(self):
        # Création du keyspace (si non existant)
        self.session.execute("""
            CREATE KEYSPACE IF NOT EXISTS gestion_etudiants 
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
        """)
        
        # Utilisation du keyspace
        self.session.set_keyspace('gestion_etudiants')
        
        # Création de la table (si non existante)
        self.session.execute("""
            CREATE TABLE IF NOT EXISTS cours (
                id UUID PRIMARY KEY,
                nom TEXT,
                enseignant TEXT
            )
        """)

    def setup_ui(self):
        title = tk.Label(self.root, text="Gestion des Cours", font=("Helvetica", 20, "bold"), bg="#B3D9FF", fg="#0A3D62")
        title.pack(pady=15)

        form_frame = tk.Frame(self.root, bg="#B3D9FF")
        form_frame.pack(pady=5)

        tk.Label(form_frame, text="Nom du cours * :", bg="#B3D9FF", fg="#0A3D62", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=10, sticky="e")
        self.entry_nom = ttk.Entry(form_frame, width=35)
        self.entry_nom.grid(row=0, column=1, padx=5, pady=10)

        tk.Label(form_frame, text="Enseignant * :", bg="#B3D9FF", fg="#0A3D62", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=10, sticky="e")
        self.entry_ens = ttk.Entry(form_frame, width=35)
        self.entry_ens.grid(row=1, column=1, padx=5, pady=10)

        btn_ajouter = ttk.Button(self.root, text="Ajouter le cours", command=self.ajouter_cours)
        btn_ajouter.pack(pady=12)

        btn_afficher = ttk.Button(self.root, text="Afficher les cours disponibles", command=self.afficher_cours)
        btn_afficher.pack()

        mandatory_label = tk.Label(self.root, text="* Champs obligatoires", bg="#B3D9FF", fg="#D63447", font=("Arial", 10, "italic"))
        mandatory_label.pack(pady=5)

    def ajouter_cours(self):
        nom = self.entry_nom.get().strip()
        enseignant = self.entry_ens.get().strip()

        if not nom or not enseignant:
            messagebox.showwarning("Champs requis", "Veuillez remplir tous les champs obligatoires.")
            return

        try:
            # Insertion dans Cassandra avec un UUID généré
            query = """
                INSERT INTO cours (id, nom, enseignant)
                VALUES (%s, %s, %s)
            """
            self.session.execute(query, (uuid1(), nom, enseignant))

            self.entry_nom.delete(0, tk.END)
            self.entry_ens.delete(0, tk.END)
            messagebox.showinfo("Succès", "Le cours a été ajouté avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout du cours: {str(e)}")

    def afficher_cours(self):
        try:
            query = "SELECT id, nom, enseignant FROM cours"
            rows = list(self.session.execute(query))

            if not rows:
                messagebox.showinfo("Info", "Aucun cours disponible pour le moment.")
                return

            popup = tk.Toplevel(self.root)
            popup.title("Cours Disponibles")
            popup.geometry("550x350")
            popup.configure(bg="#B3D9FF")

            label = tk.Label(popup, text="Liste des Cours Disponibles", font=("Helvetica", 16, "bold"), bg="#B3D9FF", fg="#0A3D62")
            label.pack(pady=10)

            tree = ttk.Treeview(popup, columns=("ID", "Nom", "Enseignant"), show="headings", height=12)
            tree.heading("ID", text="ID")
            tree.heading("Nom", text="Nom du cours")
            tree.heading("Enseignant", text="Enseignant")
            tree.column("ID", width=120, anchor="center")
            tree.column("Nom", width=180)
            tree.column("Enseignant", width=180)
            tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

            tree.tag_configure('oddrow', background='#E6F0FF')
            tree.tag_configure('evenrow', background='white')

            for idx, row in enumerate(rows):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                tree.insert("", "end", values=(str(row.id), row.nom, row.enseignant), tags=(tag,))

            btn_retour = ttk.Button(popup, text="Retour", command=popup.destroy)
            btn_retour.pack(pady=10)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des cours: {str(e)}")

    def __del__(self):
        # Fermeture de la connexion Cassandra lorsque l'application se ferme
        if hasattr(self, 'cluster'):
            self.cluster.shutdown()

if __name__ == "__main__":
    root = tk.Tk()
    app = CourseManager(root)
    root.mainloop()