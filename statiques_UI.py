# statiques.py

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from services import get_all_etudiants, get_all_cours, generate_graph_for_cours, generate_graph_for_etudiant

# Récupération des données
etudiants_dict = get_all_etudiants()
cours_dict = get_all_cours()

# Interface graphique
fenetre = tk.Tk()
fenetre.title("Statistiques Université")
fenetre.geometry("900x600")

frame_select = tk.Frame(fenetre)
frame_select.pack(pady=20)

type_var = tk.StringVar()
type_select = ttk.Combobox(frame_select, textvariable=type_var, state='readonly', values=["Étudiant", "Cours"])
type_select.grid(row=0, column=0, padx=10)
type_select.set("Choisir...")

item_var = tk.StringVar()
item_select = ttk.Combobox(frame_select, textvariable=item_var, state='readonly')
item_select.grid(row=0, column=1, padx=10)

canvas_frame = tk.Frame(fenetre)
canvas_frame.pack()

info_label = tk.Label(fenetre, text="", font=("Arial", 12))
info_label.pack(pady=10)

def afficher_resultat(*args):
    for widget in canvas_frame.winfo_children():
        widget.destroy()
    info_label.config(text="")

    if type_var.get() == "Cours":
        cours_id = cours_dict.get(item_var.get())
        fig, meilleure_note = generate_graph_for_cours(cours_id)

        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        info_label.config(text=f"✅ Meilleure note dans ce cours : {meilleure_note}/20")

    elif type_var.get() == "Étudiant":
        etu_id = etudiants_dict.get(item_var.get())
        fig, moyenne = generate_graph_for_etudiant(etu_id)

        if fig:
            canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()

        info_label.config(text=f"🎓 Moyenne générale de {item_var.get()} : {moyenne}/20")

def update_item_select(*args):
    if type_var.get() == "Étudiant":
        item_select.config(values=list(etudiants_dict.keys()))
    elif type_var.get() == "Cours":
        item_select.config(values=list(cours_dict.keys()))
    item_select.set("")

type_select.bind("<<ComboboxSelected>>", update_item_select)
item_select.bind("<<ComboboxSelected>>", afficher_resultat)

fenetre.mainloop()
