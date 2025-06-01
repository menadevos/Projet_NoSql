import tkinter as tk
from tkinter import ttk, messagebox
from cassandra.cluster import Cluster
from uuid import uuid1
import subprocess


def create_interface_cours(parent):
    """Crée et retourne l'interface de gestion des cours intégrée dans le parent donné"""
    # On crée un conteneur Frame qui va accueillir le CourseManager
    container = tk.Frame(parent)
    
    # On adapte le CourseManager pour qu'il utilise ce container comme racine
    # plutôt que de créer sa propre fenêtre Tk()
    manager = CourseManager(container)  # On passe le container comme racine
    
    # On s'assure que le manager remplit tout l'espace disponible
    container.pack(fill="both", expand=True)
    
    return container


class CourseManager:
    def __init__(self, root):
        # CORRECTION: Assigner self.root en premier
        self.root = root
        
        self.colors = {
            'vanilla_ice': '#F8F6F0',      # Fond principal
            'cosmic': '#2E1065',           # Bleu violet foncé
            'provincial': '#16537e',       # Bleu-vert
            'grape': '#7C3AED',            # Violet
            'light_grape': '#A78BFA',      # Violet clair
            'accent': '#F3F4F6',           # Gris très clair
            'text_dark': '#1F2937',        # Texte foncé
            'text_light': '#6B7280',       # Texte clair
            'success': '#10B981',          # Vert succès
            'warning': '#F59E0B',          # Orange warning
            'danger': '#EF4444'            # Rouge danger
        }

        if isinstance(self.root, (tk.Tk, tk.Toplevel)):
            self.root.title("Gestion des Cours")
            self.root.geometry("600x400")
            self.root.configure(bg=self.colors['vanilla_ice'])

        # Connexion à Cassandra avec gestion d'erreur
        try:
            self.cluster = Cluster(['127.0.0.1'])
            self.session = self.cluster.connect()
            self.setup_database()
        except Exception as e:
            messagebox.showerror("Erreur de connexion", 
                               f"Impossible de se connecter à Cassandra: {str(e)}\n"
                               "Assurez-vous que Cassandra est démarré.")
            # Initialiser des valeurs par défaut pour éviter les erreurs
            self.cluster = None
            self.session = None
        
        self.style_buttons()
        self.setup_ui()

    def style_buttons(self):
        style = ttk.Style()
        style.theme_use('default')

        # Bouton vert succès
        style.configure("Success.TButton",
                        background=self.colors['success'],
                        foreground="white",
                        font=("Arial", 11, "bold"),
                        padding=6)
        style.map("Success.TButton",
                  background=[('active', '#0f9d71')])

        # Bouton rouge danger (Retour)
        style.configure("Danger.TButton",
                        background=self.colors['danger'],
                        foreground="white",
                        font=("Arial", 11, "bold"),
                        padding=6)
        style.map("Danger.TButton",
                  background=[('active', '#d13c3c')])

        # Treeview style
        style.configure("Treeview",
                        background=self.colors['accent'],
                        foreground=self.colors['text_dark'],
                        rowheight=25,
                        fieldbackground=self.colors['vanilla_ice'],
                        font=("Arial", 10))
        style.map('Treeview', background=[('selected', self.colors['grape'])], foreground=[('selected', 'white')])

        # Scrollbar style (optionnel)
        style.configure("Vertical.TScrollbar",
                        troughcolor=self.colors['vanilla_ice'],
                        background=self.colors['grape'],
                        bordercolor=self.colors['vanilla_ice'],
                        arrowcolor=self.colors['grape'])

    def setup_database(self):
        if self.session is None:
            return
        try:
            self.session.execute("""
                CREATE KEYSPACE IF NOT EXISTS gestion_etudiants 
                WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
            """)
            self.session.set_keyspace('gestion_etudiants')
            self.session.execute("""
                CREATE TABLE IF NOT EXISTS cours (
                    id UUID PRIMARY KEY,
                    nom TEXT,
                    enseignant TEXT
                )
            """)
        except Exception as e:
            messagebox.showerror("Erreur de base de données", 
                               f"Erreur lors de la configuration de la base de données: {str(e)}")

    def setup_ui(self):
        title = tk.Label(self.root, text="Gestion des Cours", 
                         font=("Helvetica", 22, "bold"), 
                         bg=self.colors['vanilla_ice'], 
                         fg=self.colors['cosmic'])
        title.pack(pady=20)

        form_frame = tk.Frame(self.root, bg=self.colors['vanilla_ice'])
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Nom du cours * :", 
                 bg=self.colors['vanilla_ice'], fg=self.colors['text_dark'], 
                 font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=10, sticky="e")
        self.entry_nom = ttk.Entry(form_frame, width=40)
        self.entry_nom.grid(row=0, column=1, padx=5, pady=10)

        tk.Label(form_frame, text="Enseignant * :", 
                 bg=self.colors['vanilla_ice'], fg=self.colors['text_dark'], 
                 font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=10, sticky="e")
        self.entry_ens = ttk.Entry(form_frame, width=40)
        self.entry_ens.grid(row=1, column=1, padx=5, pady=10)

        btn_ajouter = ttk.Button(self.root, text="Ajouter le cours", 
                                 command=self.ajouter_cours, style="Success.TButton")
        btn_ajouter.pack(pady=12)

        btn_afficher = ttk.Button(self.root, text="Afficher les cours disponibles", 
                                  command=self.afficher_cours, style="Success.TButton")
        btn_afficher.pack()

        btn_retour_main = ttk.Button(self.root, text="Retour", 
                                     command=self.retour_main_interface, style="Danger.TButton")
        btn_retour_main.pack(pady=15)

        mandatory_label = tk.Label(self.root, text="* Champs obligatoires", 
                                   bg=self.colors['vanilla_ice'], fg=self.colors['danger'], 
                                   font=("Arial", 10, "italic"))
        mandatory_label.pack(pady=5)

    def ajouter_cours(self):
        if self.session is None:
            messagebox.showerror("Erreur", "Aucune connexion à la base de données disponible.")
            return
            
        nom = self.entry_nom.get().strip()
        enseignant = self.entry_ens.get().strip()

        if not nom or not enseignant:
            messagebox.showwarning("Champs requis", "Veuillez remplir tous les champs obligatoires.")
            return

        try:
            query = """
                INSERT INTO cours (id, nom, enseignant)
                VALUES (%s, %s, %s)
            """
            self.session.execute(query, (uuid1(), nom, enseignant))
            self.entry_nom.delete(0, tk.END)
            self.entry_ens.delete(0, tk.END)
            messagebox.showinfo("Succès", "Le cours a été ajouté avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", "Erreur lors de l'ajout du cours: " + str(e))

    def afficher_cours(self):
        if self.session is None:
            messagebox.showerror("Erreur", "Aucune connexion à la base de données disponible.")
            return
            
        try:
            query = "SELECT id, nom, enseignant FROM cours"
            rows = list(self.session.execute(query))

            if not rows:
                messagebox.showinfo("Info", "Aucun cours disponible pour le moment.")
                return

            popup = tk.Toplevel(self.root)
            popup.title("Cours Disponibles")
            popup.geometry("600x400")
            popup.configure(bg=self.colors['vanilla_ice'])

            label = tk.Label(popup, text="Liste des Cours Disponibles", 
                             font=("Helvetica", 16, "bold"), 
                             bg=self.colors['vanilla_ice'], fg=self.colors['cosmic'])
            label.pack(pady=10)

            tree = ttk.Treeview(popup, columns=("ID", "Nom", "Enseignant"), show="headings", height=12)
            tree.heading("ID", text="ID court")
            tree.heading("Nom", text="Nom du cours")
            tree.heading("Enseignant", text="Enseignant")
            tree.column("ID", width=120, anchor="center")
            tree.column("Nom", width=220)
            tree.column("Enseignant", width=220)
            tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

            tree.tag_configure('oddrow', background=self.colors['accent'])
            tree.tag_configure('evenrow', background='white')

            for idx, row in enumerate(rows):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                short_id = str(row.id)[:8]
                tree.insert("", "end", values=(short_id, row.nom, row.enseignant), tags=(tag,))

            btn_retour = ttk.Button(popup, text="Retour", command=popup.destroy, style="Success.TButton")
            btn_retour.pack(pady=10)

        except Exception as e:
            messagebox.showerror("Erreur", "Erreur lors de la récupération des cours: " + str(e))

    def retour_main_interface(self):
        # Au lieu de détruire et relancer, on peut simplement signaler au parent
        # qu'on veut revenir au menu principal
        # Cette fonction sera remplacée par la fonction du parent si nécessaire
        if hasattr(self, 'parent_callback') and self.parent_callback:
            self.parent_callback()
        else:
            # Fallback: fermer la fenêtre actuelle si c'est une fenêtre indépendante
            if isinstance(self.root, (tk.Tk, tk.Toplevel)):
                self.root.destroy()
                subprocess.Popen(["python", "main_interface.py"])

    def __del__(self):
        if hasattr(self, 'cluster'):
            self.cluster.shutdown()


if __name__ == "__main__":
    root = tk.Tk()
    app = CourseManager(root)
    root.mainloop()