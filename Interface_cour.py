import Tkinter as tk
import tkMessageBox as messagebox
import ttk
from cassandra.cluster import Cluster
from uuid import uuid1
import subprocess
import threading
import time

class AnimatedLabel(tk.Label):
    def __init__(self, parent, text, **kwargs):
        tk.Label.__init__(self, parent, text=text, **kwargs)
        self.original_text = text
        self.dots = 0
        
    def animate_loading(self):
        self.dots = (self.dots + 1) % 4
        self.config(text=self.original_text + "." * self.dots)
        self.after(500, self.animate_loading)

class CourseManager:
    def __init__(self, root):
        self.colors = {
            'primary': '#1a365d',
            'secondary': '#2d3748', 
            'accent': '#4299e1',
            'accent_hover': '#3182ce',
            'success': '#38a169',
            'success_hover': '#2f855a',
            'danger': '#e53e3e',
            'danger_hover': '#c53030',
            'warning': '#d69e2e',
            'background': '#f7fafc',
            'surface': '#ffffff',
            'surface_alt': '#edf2f7',
            'text_primary': '#1a202c',
            'text_secondary': '#4a5568',
            'text_muted': '#718096',
            'border': '#e2e8f0',
            'shadow': '#00000010'
        }

        self.root = root
        self.root.title("Systeme de Gestion des Cours - Version Professionnelle")
        self.root.geometry("750x550")
        self.root.configure(bg=self.colors['background'])
        self.root.resizable(True, True)
        
        self.center_window()
        
        self.cluster = Cluster(['127.0.0.1'])
        self.session = self.cluster.connect()
        self.loading = False

        self.setup_database()
        self.configure_styles()
        self.create_interface()
        
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        pos_x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        pos_y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, pos_x, pos_y))

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("Primary.TButton",
                        background=self.colors['accent'],
                        foreground="white",
                        font=("Segoe UI", 11, "bold"),
                        padding=(20, 10),
                        relief="flat",
                        borderwidth=0)
        style.map("Primary.TButton",
                  background=[('active', self.colors['accent_hover']),
                             ('pressed', self.colors['primary'])])

        style.configure("Success.TButton",
                        background=self.colors['success'],
                        foreground="white",
                        font=("Segoe UI", 11, "bold"),
                        padding=(20, 10),
                        relief="flat",
                        borderwidth=0)
        style.map("Success.TButton",
                  background=[('active', self.colors['success_hover'])])

        style.configure("Danger.TButton",
                        background=self.colors['danger'],
                        foreground="white",
                        font=("Segoe UI", 11, "bold"),
                        padding=(15, 8),
                        relief="flat",
                        borderwidth=0)
        style.map("Danger.TButton",
                  background=[('active', self.colors['danger_hover'])])

        style.configure("Card.TFrame",
                        background=self.colors['surface'],
                        relief="solid",
                        borderwidth=1)

        style.configure("Modern.TEntry",
                        padding=(10, 8),
                        font=("Segoe UI", 11),
                        borderwidth=2,
                        relief="flat")
        style.map("Modern.TEntry",
                  bordercolor=[('focus', self.colors['accent'])])

        style.configure("Header.Treeview",
                        background=self.colors['surface'],
                        foreground=self.colors['text_primary'],
                        rowheight=35,
                        fieldbackground=self.colors['surface'],
                        font=("Segoe UI", 10))
        
        style.configure("Header.Treeview.Heading",
                        background=self.colors['primary'],
                        foreground="white",
                        font=("Segoe UI", 11, "bold"),
                        padding=(10, 8))
        
        style.map('Header.Treeview', 
                  background=[('selected', self.colors['accent'])],
                  foreground=[('selected', 'white')])

    def setup_database(self):
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
                    enseignant TEXT,
                    date_creation TIMESTAMP
                )
            """)
        except Exception as e:
            messagebox.showerror("Erreur de Base de Donnees", 
                               "Impossible de configurer la base de donnees:\n" + str(e))

    def create_interface(self):
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.create_header(main_container)
        self.create_form_section(main_container)
        self.create_action_buttons(main_container)
        self.create_status_bar()

    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg=self.colors['background'])
        header_frame.pack(fill=tk.X, pady=(0, 30))

        title_frame = tk.Frame(header_frame, bg=self.colors['primary'], relief="flat")
        title_frame.pack(fill=tk.X, ipady=20)

        title = tk.Label(title_frame, 
                        text="GESTION DES COURS",
                        font=("Segoe UI", 24, "bold"),
                        bg=self.colors['primary'],
                        fg="white")
        title.pack()

        subtitle = tk.Label(title_frame,
                           text="Systeme de Gestion Academique",
                           font=("Segoe UI", 12),
                           bg=self.colors['primary'],
                           fg=self.colors['surface_alt'])
        subtitle.pack(pady=(5, 0))

    def create_form_section(self, parent):
        form_container = ttk.Frame(parent, style="Card.TFrame")
        form_container.pack(fill=tk.X, pady=(0, 20), ipady=20, ipadx=20)

        form_title = tk.Label(form_container,
                             text="Ajouter un Nouveau Cours",
                             font=("Segoe UI", 16, "bold"),
                             bg=self.colors['surface'],
                             fg=self.colors['text_primary'])
        form_title.pack(pady=(0, 20))

        form_frame = tk.Frame(form_container, bg=self.colors['surface'])
        form_frame.pack(fill=tk.X)

        tk.Label(form_frame, 
                text="Nom du Cours",
                font=("Segoe UI", 12, "bold"),
                bg=self.colors['surface'],
                fg=self.colors['text_primary']).grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.entry_nom = ttk.Entry(form_frame, width=50, style="Modern.TEntry")
        self.entry_nom.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        tk.Label(form_frame,
                text="Nom de l'Enseignant",
                font=("Segoe UI", 12, "bold"),
                bg=self.colors['surface'],
                fg=self.colors['text_primary']).grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        self.entry_ens = ttk.Entry(form_frame, width=50, style="Modern.TEntry")
        self.entry_ens.grid(row=3, column=0, sticky="ew", pady=(0, 15))

        form_frame.grid_columnconfigure(0, weight=1)

        required_note = tk.Label(form_container,
                                text="* Tous les champs sont obligatoires",
                                font=("Segoe UI", 10, "italic"),
                                bg=self.colors['surface'],
                                fg=self.colors['danger'])
        required_note.pack(pady=(10, 0))

    def create_action_buttons(self, parent):
        button_frame = tk.Frame(parent, bg=self.colors['background'])
        button_frame.pack(fill=tk.X, pady=(0, 10))

        buttons_container = tk.Frame(button_frame, bg=self.colors['background'])
        buttons_container.pack()

        btn_add = ttk.Button(buttons_container,
                            text=" AJOUTER LE COURS",
                            command=self.ajouter_cours_avec_animation,
                            style="Success.TButton")
        btn_add.pack(side=tk.LEFT, padx=(0, 15))

        btn_view = ttk.Button(buttons_container,
                             text=" VOIR LES COURS",
                             command=self.afficher_cours,
                             style="Primary.TButton")
        btn_view.pack(side=tk.LEFT, padx=(0, 15))

        btn_return = ttk.Button(buttons_container,
                               text="RETOUR",
                               command=self.retour_main_interface,
                               style="Danger.TButton")
        btn_return.pack(side=tk.LEFT)

    def create_status_bar(self):
        self.status_frame = tk.Frame(self.root, bg=self.colors['primary'], height=30)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_frame.pack_propagate(False)

        self.status_label = tk.Label(self.status_frame,
                                    text="Pret - En attente d'action utilisateur",
                                    font=("Segoe UI", 10),
                                    bg=self.colors['primary'],
                                    fg="white")
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)

    def update_status(self, message, color=None):
        if color:
            self.status_frame.config(bg=color)
            self.status_label.config(bg=color)
        else:
            self.status_frame.config(bg=self.colors['primary'])
            self.status_label.config(bg=self.colors['primary'])
        self.status_label.config(text=message)
        self.root.update()

    def ajouter_cours_avec_animation(self):
        if self.loading:
            return
            
        nom = self.entry_nom.get().strip()
        enseignant = self.entry_ens.get().strip()

        if not nom or not enseignant:
            self.update_status("Erreur: Veuillez remplir tous les champs", self.colors['danger'])
            messagebox.showwarning("Champs Requis", 
                                 "Veuillez remplir tous les champs obligatoires.")
            self.root.after(3000, lambda: self.update_status("Pret - En attente d'action utilisateur"))
            return

        self.loading = True
        self.update_status("Ajout du cours en cours...", self.colors['warning'])
        
        def ajouter_async():
            try:
                time.sleep(0.5)
                query = """
                    INSERT INTO cours (id, nom, enseignant, date_creation)
                    VALUES (%s, %s, %s, toTimestamp(now()))
                """
                self.session.execute(query, (uuid1(), nom, enseignant))
                
                self.root.after(0, self.on_ajout_success)
                
            except Exception as e:
                self.root.after(0, lambda: self.on_ajout_error(str(e)))

        thread = threading.Thread(target=ajouter_async)
        thread.daemon = True
        thread.start()

    def on_ajout_success(self):
        self.entry_nom.delete(0, tk.END)
        self.entry_ens.delete(0, tk.END)
        self.update_status("Cours ajoute avec succes!", self.colors['success'])
        messagebox.showinfo("Succes", "Le cours a ete ajoute avec succes dans la base de donnees.")
        self.loading = False
        self.root.after(3000, lambda: self.update_status("Pret - En attente d'action utilisateur"))

    def on_ajout_error(self, error):
        self.update_status("Erreur lors de l'ajout", self.colors['danger'])
        messagebox.showerror("Erreur", "Erreur lors de l'ajout du cours:\n" + error)
        self.loading = False
        self.root.after(3000, lambda: self.update_status("Pret - En attente d'action utilisateur"))

    def afficher_cours(self):
        self.update_status("Chargement des cours...", self.colors['warning'])
        
        try:
            query = "SELECT id, nom, enseignant FROM cours"
            rows = list(self.session.execute(query))

            if not rows:
                self.update_status("Aucun cours trouve", self.colors['warning'])
                messagebox.showinfo("Information", "Aucun cours disponible pour le moment.")
                self.root.after(2000, lambda: self.update_status("Pret - En attente d'action utilisateur"))
                return

            self.create_cours_window(rows)
            self.update_status("Liste des cours affichee", self.colors['success'])
            self.root.after(2000, lambda: self.update_status("Pret - En attente d'action utilisateur"))

        except Exception as e:
            self.update_status("Erreur de chargement", self.colors['danger'])
            messagebox.showerror("Erreur", "Erreur lors de la recuperation des cours:\n" + str(e))
            self.root.after(3000, lambda: self.update_status("Pret - En attente d'action utilisateur"))

    def create_cours_window(self, rows):
        popup = tk.Toplevel(self.root)
        popup.title("Liste des Cours Disponibles")
        popup.geometry("800x500")
        popup.configure(bg=self.colors['background'])
        popup.transient(self.root)
        popup.grab_set()

        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (popup.winfo_width() // 2)
        y = (popup.winfo_screenheight() // 2) - (popup.winfo_height() // 2)
        popup.geometry('+{}+{}'.format(x, y))

        header_frame = tk.Frame(popup, bg=self.colors['primary'])
        header_frame.pack(fill=tk.X, pady=(0, 20))

        title = tk.Label(header_frame,
                        text="COURS DISPONIBLES",
                        font=("Segoe UI", 18, "bold"),
                        bg=self.colors['primary'],
                        fg="white")
        title.pack(pady=15)

        count_label = tk.Label(header_frame,
                              text="Total: {} cours enregistres".format(len(rows)),
                              font=("Segoe UI", 11),
                              bg=self.colors['primary'],
                              fg=self.colors['surface_alt'])
        count_label.pack(pady=(0, 10))

        tree_frame = tk.Frame(popup, bg=self.colors['background'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        tree = ttk.Treeview(tree_frame, 
                           columns=("ID", "Nom", "Enseignant"), 
                           show="headings", 
                           height=15,
                           style="Header.Treeview")
        
        tree.heading("ID", text="ID COURS")
        tree.heading("Nom", text="NOM DU COURS")
        tree.heading("Enseignant", text="ENSEIGNANT")
        
        tree.column("ID", width=120, anchor="center", minwidth=100)
        tree.column("Nom", width=250, anchor="w", minwidth=200)
        tree.column("Enseignant", width=250, anchor="w", minwidth=200)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tree.tag_configure('odd', background=self.colors['surface_alt'])
        tree.tag_configure('even', background=self.colors['surface'])

        for idx, row in enumerate(rows):
            tag = 'even' if idx % 2 == 0 else 'odd'
            short_id = str(row.id)[:8].upper()
            tree.insert("", "end", values=(short_id, row.nom, row.enseignant), tags=(tag,))

        button_frame = tk.Frame(popup, bg=self.colors['background'])
        button_frame.pack(pady=10)

        btn_close = ttk.Button(button_frame,
                              text=" FERMER",
                              command=popup.destroy,
                              style="Primary.TButton")
        btn_close.pack()

    def retour_main_interface(self):
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment quitter l'application?"):
            self.root.destroy()
            try:
                subprocess.Popen(["python", "main_interface.py"])
            except:
                pass

    def __del__(self):
        if hasattr(self, 'cluster'):
            self.cluster.shutdown()

if __name__ == "__main__":
    root = tk.Tk()
    try:
        app = CourseManager(root)
        root.mainloop()
    except KeyboardInterrupt:
        root.quit()
    except Exception as e:
        messagebox.showerror("Erreur Critique", "Une erreur critique s'est produite:\n" + str(e))
        root.quit()