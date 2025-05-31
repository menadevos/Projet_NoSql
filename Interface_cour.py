import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class CourseManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Cours")
        self.root.geometry("500x320")
        self.root.configure(bg="#B3D9FF")

        self.courses = []
        self.course_id = 1

        self.load_courses()  # Charger les cours depuis fichier

        self.setup_ui()

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

        # Ajouter dans la liste
        self.courses.append((self.course_id, nom, enseignant))
        self.course_id += 1

        # Sauvegarder dans fichier JSON
        self.save_courses()

        self.entry_nom.delete(0, tk.END)
        self.entry_ens.delete(0, tk.END)

        messagebox.showinfo("Succès", "Le cours a été ajouté avec succès.")

    def afficher_cours(self):
        if not self.courses:
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
        tree.column("ID", width=60, anchor="center")
        tree.column("Nom", width=220)
        tree.column("Enseignant", width=220)
        tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        tree.tag_configure('oddrow', background='#E6F0FF')
        tree.tag_configure('evenrow', background='white')

        for idx, course in enumerate(self.courses):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            tree.insert("", "end", values=course, tags=(tag,))

        btn_retour = ttk.Button(popup, text="Retour", command=popup.destroy)
        btn_retour.pack(pady=10)

    def save_courses(self):
        # On convertit les tuples en liste pour JSON
        with open("cours.json", "w", encoding="utf-8") as f:
            json.dump([list(c) for c in self.courses], f, ensure_ascii=False, indent=4)

    def load_courses(self):
        if os.path.exists("cours.json"):
            with open("cours.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.courses = [tuple(c) for c in data]
                # Remettre à jour l'ID pour éviter les doublons
                if self.courses:
                    self.course_id = max(c[0] for c in self.courses) + 1

if __name__ == "__main__":
    root = tk.Tk()
    app = CourseManager(root)
    root.mainloop()
