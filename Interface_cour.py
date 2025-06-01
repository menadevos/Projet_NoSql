import tkinter as tk
from tkinter import ttk, messagebox
from cassandra.cluster import Cluster
from uuid import uuid1
from cours import CoursService
from cassandra_connexion import CassandraConnection
def create_interface_cours(parent):
    container = tk.Frame(parent)
    manager = CourseManager(container)
    container.pack(fill="both", expand=True)
    return container



class CourseManager:
    def __init__(self, root):
        self.root = root
        self.colors = {
            'vanilla_ice': '#F8F6F0',
            'cosmic': '#2E1065',
            'provincial': '#16537e',
            'grape': '#7C3AED',
            'light_grape': '#A78BFA',
            'accent': '#F3F4F6',
            'text_dark': '#1F2937',
            'text_light': '#6B7280',
            'success': '#10B981',
            'warning': '#F59E0B',
            'danger': '#EF4444'
        }

        if isinstance(self.root, (tk.Tk, tk.Toplevel)):
            self.root.title("Gestion des Cours")
            self.root.geometry("700x450")
            self.root.configure(bg=self.colors['vanilla_ice'])

        try:
               connexion = CassandraConnection()
               self.session = connexion.get_session()

               if not self.session:
                  raise Exception("Session Cassandra introuvable.")
               self.service = CoursService(self.session)
        except Exception as e:
            messagebox.showerror("Erreur de connexion",
                                 f"Impossible de se connecter à Cassandra: {str(e)}\n"
                                 "Assurez-vous que Cassandra est démarré.")
            
            self.session = None

        self.style_buttons()

        self.main_frame = tk.Frame(self.root, bg=self.colors['vanilla_ice'])
        self.main_frame.pack(fill="both", expand=True)

        self.cours_frame = tk.Frame(self.main_frame, bg=self.colors['vanilla_ice'])
        self.cours_frame.pack(fill="both", expand=True)

        self.form_frame = tk.Frame(self.main_frame, bg=self.colors['vanilla_ice'])

        self.setup_ui()
        self.afficher_cours_direct()

    def style_buttons(self):
        style = ttk.Style()
        style.theme_use('default')

        style.configure("Success.TButton",
                        background=self.colors['success'],
                        foreground="white",
                        font=("Arial", 11, "bold"),
                        padding=6)
        style.map("Success.TButton", background=[('active', '#0f9d71')])

        style.configure("Danger.TButton",
                        background=self.colors['danger'],
                        foreground="white",
                        font=("Arial", 11, "bold"),
                        padding=6)
        style.map("Danger.TButton", background=[('active', '#d13c3c')])

        style.configure("Treeview",
                        background=self.colors['accent'],
                        foreground=self.colors['text_dark'],
                        rowheight=50,
                        fieldbackground=self.colors['vanilla_ice'],
                        font=("Arial", 15))
        style.map('Treeview',
                  background=[('selected', self.colors['grape'])],
                  foreground=[('selected', 'white')])

        style.configure("Treeview.Heading",
                        font=("Arial", 11, "bold"),
                        background=self.colors['cosmic'],
                        foreground="white")

 
    def setup_ui(self):
        header_frame = tk.Frame(self.cours_frame, bg=self.colors['vanilla_ice'])
        header_frame.pack(fill='x', pady=(15, 5), padx=15)

        title = tk.Label(header_frame, text="Liste des Cours",
                         font=("Helvetica", 22, "bold"),
                         bg=self.colors['vanilla_ice'],
                         fg=self.colors['cosmic'])
        title.pack(side='left')

        btn_ajouter = ttk.Button(header_frame, text="Ajouter un nouveau cours",
                                 command=self.afficher_formulaire_ajout,
                                 style="Success.TButton")
        btn_ajouter.pack(side='right')

        self.tree = ttk.Treeview(self.cours_frame, columns=("ID", "Nom", "Enseignant"), show="headings", height=15)
        self.tree.heading("ID", text="ID court")
        self.tree.heading("Nom", text="Nom du cours")
        self.tree.heading("Enseignant", text="Enseignant")
        self.tree.column("ID", width=120, anchor="center")
        self.tree.column("Nom", width=250)
        self.tree.column("Enseignant", width=250)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.tree.tag_configure('oddrow', background=self.colors['accent'])
        self.tree.tag_configure('evenrow', background='white')

        scrollbar = ttk.Scrollbar(self.cours_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        self.build_formulaire()

    def afficher_cours_direct(self):
        self.form_frame.pack_forget()
        self.cours_frame.pack(fill="both", expand=True)

        try:
            rows = self.service.get_all_cours()
            for item in self.tree.get_children():
                self.tree.delete(item)
            if not rows:
                self.tree.insert("", "end", values=("", "Aucun cours disponible", ""), tags=('oddrow',))
                return
            for idx, row in enumerate(rows):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                short_id = str(row.id)[:8]
                self.tree.insert("", "end", values=(short_id, row.nom, row.enseignant), tags=(tag,))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des cours: {str(e)}")



    def build_formulaire(self):
        for widget in self.form_frame.winfo_children():
            widget.destroy()

        card_frame = tk.Frame(self.form_frame, bg="white", bd=2, relief="groove")
        card_frame.pack(padx=40, pady=30, fill="x", ipadx=20, ipady=20)

        title = tk.Label(card_frame, text="Ajouter un nouveau cours",
                         font=("Helvetica", 22, "bold"),
                         bg="white", fg=self.colors['cosmic'])
        title.pack(pady=(0, 25))

        form_inner = tk.Frame(card_frame, bg="white")
        form_inner.pack(padx=20, pady=10)

        label_font = ("Arial", 14)
        entry_font = ("Arial", 13)

        tk.Label(form_inner, text="Nom du cours * :", bg="white",
                 fg=self.colors['text_dark'], font=label_font).grid(row=0, column=0, sticky="e", pady=12, padx=15)
        self.entry_nom = ttk.Entry(form_inner, width=45, font=entry_font)
        self.entry_nom.grid(row=0, column=1, pady=12)

        tk.Label(form_inner, text="Enseignant * :", bg="white",
                 fg=self.colors['text_dark'], font=label_font).grid(row=1, column=0, sticky="e", pady=12, padx=15)
        self.entry_ens = ttk.Entry(form_inner, width=45, font=entry_font)
        self.entry_ens.grid(row=1, column=1, pady=12)

        btn_frame = tk.Frame(card_frame, bg="white")
        btn_frame.pack(pady=30)

        btn_save = ttk.Button(btn_frame, text="Ajouter", command=self.ajouter_cours, style="Success.TButton")
        btn_save.pack(side="left", padx=15)

        btn_cancel = ttk.Button(btn_frame, text="Annuler", command=self.annuler_ajout, style="Danger.TButton")
        btn_cancel.pack(side="left", padx=15)

    def afficher_formulaire_ajout(self):
        self.cours_frame.pack_forget()
        self.form_frame.pack(fill="both", expand=True)
        self.entry_nom.delete(0, tk.END)
        self.entry_ens.delete(0, tk.END)

    def annuler_ajout(self):
        self.form_frame.pack_forget()
        self.cours_frame.pack(fill="both", expand=True)

    def ajouter_cours(self):
        nom = self.entry_nom.get().strip()
        enseignant = self.entry_ens.get().strip()

        if not nom or not enseignant:
            messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs.")
            return

        try:
            self.service.ajouter_cours(nom, enseignant)
            messagebox.showinfo("Succès", "Cours ajouté avec succès.")
            self.afficher_cours_direct()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l’ajout du cours : {str(e)}")



if __name__ == "__main__":
    root = tk.Tk()
    create_interface_cours(root)
    root.mainloop()

