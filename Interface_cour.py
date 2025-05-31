import tkinter as tk
from tkinter import ttk, messagebox

class CourseManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Cours")
        self.root.geometry("600x400")
        self.root.configure(bg="#f5f5f5")

        self.courses = []
        self.course_id = 1

        self.setup_ui()

    def setup_ui(self):
        # Titre
        title = tk.Label(self.root, text="Gestion des Cours", font=("Helvetica", 18, "bold"), bg="#f5f5f5", fg="#333")
        title.pack(pady=10)

        # Zone formulaire
        form_frame = tk.Frame(self.root, bg="#f5f5f5")
        form_frame.pack(pady=5)

        tk.Label(form_frame, text="Nom du cours :", bg="#f5f5f5").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_nom = ttk.Entry(form_frame, width=30)
        self.entry_nom.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Enseignant :", bg="#f5f5f5").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_ens = ttk.Entry(form_frame, width=30)
        self.entry_ens.grid(row=1, column=1, padx=5, pady=5)

        btn_ajouter = ttk.Button(self.root, text="Ajouter le cours", command=self.ajouter_cours)
        btn_ajouter.pack(pady=10)

        # Tableau des cours
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nom", "Enseignant"), show="headings", height=8)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nom", text="Nom du cours")
        self.tree.heading("Enseignant", text="Enseignant")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nom", width=200)
        self.tree.column("Enseignant", width=200)
        self.tree.pack(pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.place(x=575, y=180, height=180)

    def ajouter_cours(self):
        nom = self.entry_nom.get().strip()
        enseignant = self.entry_ens.get().strip()

        if not nom or not enseignant:
            messagebox.showwarning("Champs requis", "Veuillez remplir tous les champs.")
            return

        self.tree.insert("", "end", values=(self.course_id, nom, enseignant))
        self.course_id += 1

        self.entry_nom.delete(0, tk.END)
        self.entry_ens.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CourseManager(root)
    root.mainloop()
