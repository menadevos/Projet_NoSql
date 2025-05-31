import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def lancer_ui():
    root = tk.Tk()
    root.title("Application Gestion Étudiants")
    root.geometry("900x600")
    root.configure(bg="#F5F7FA")  # couleur de fond claire

    # ===== NAVBAR =====
    navbar = tk.Frame(root, bg="#000000", height=60)
    navbar.pack(fill="x")

    # Logo à gauche dans la navbar
    logo_img = Image.open("logo-white.png")  # mets ton chemin exact ici si différent
    logo_img = logo_img.resize((40, 40))
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(navbar, image=logo_photo, bg="#000000")
    logo_label.image = logo_photo
    logo_label.pack(side="left", padx=20, pady=10)

    # ===== CONTENU PRINCIPAL =====
    frame_contenu = tk.Frame(root, bg="#F5F7FA")
    frame_contenu.pack(expand=True)

    titre = tk.Label(
        frame_contenu,
        text="Bienvenue dans l'application de gestion académique",
        font=("Helvetica", 20, "bold"),
        bg="#F5F7FA",
        fg="#2C3E50"
    )
    titre.pack(pady=30)

    # Style commun des boutons
    style_btn = {
        "font": ("Helvetica", 16, "bold"),
        "width": 30,
        "height": 2,
        "bg": "#2980B9",
        "fg": "white",
        "activebackground": "#1F618D",
        "bd": 0,
        "relief": "flat",
        "cursor": "hand2"
    }

    btn1 = tk.Button(frame_contenu, text="👨‍🎓 Gestion des Étudiants", **style_btn, command=ouvrir_gestion_etudiants)
    btn2 = tk.Button(frame_contenu, text="📘 Gestion des Cours", **style_btn, command=ouvrir_gestion_cours)
    btn3 = tk.Button(frame_contenu, text="📝 Gestion des Notes", **style_btn, command=ouvrir_gestion_notes)

    btn1.pack(pady=15)
    btn2.pack(pady=15)
    btn3.pack(pady=15)

    # ===== FOOTER =====
    # ===== FOOTER =====
    footer = tk.Frame(root, bg="#2C3E50", height=120)
    footer.pack(fill="x", side="bottom")

    # 3 colonnes dans le footer
    colonne1 = tk.Frame(footer, bg="#2C3E50")
    colonne2 = tk.Frame(footer, bg="#2C3E50")
    colonne3 = tk.Frame(footer, bg="#2C3E50")

    colonne1.pack(side="left", expand=True, padx=30, pady=20)
    colonne2.pack(side="left", expand=True, padx=30, pady=20)
    colonne3.pack(side="left", expand=True, padx=30, pady=20)

    # Colonne 1 : Logo + Nom
    logo_img = Image.open("images.png")  # mets le logo dans le même dossier
    logo_img = logo_img.resize((60, 60))
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(colonne1, image=logo_photo, bg="#2C3E50")
    logo_label.image = logo_photo
    logo_label.pack()

    nom_faculte = tk.Label(colonne1, text="FST Tanger", font=("Helvetica", 14, "bold"), fg="white", bg="#2C3E50")
    nom_faculte.pack()

    # Colonne 2 : Contact
    contact_title = tk.Label(colonne2, text="CONTACT", font=("Helvetica", 12, "bold"), fg="white", bg="#2C3E50")
    contact_title.pack(anchor="w")

    contact_email = tk.Label(colonne2, text="contact@fstt.ma", fg="white", bg="#2C3E50", font=("Helvetica", 10))
    contact_email.pack(anchor="w", pady=2)

    contact_tel = tk.Label(colonne2, text="+212 5 39 39 39 39", fg="white", bg="#2C3E50", font=("Helvetica", 10))
    contact_tel.pack(anchor="w")

    # Colonne 3 : Liens importants
    liens_title = tk.Label(colonne3, text="LIENS UTILES", font=("Helvetica", 12, "bold"), fg="white", bg="#2C3E50")
    liens_title.pack(anchor="w")

    lien1 = tk.Label(colonne3, text="🏠 Accueil", fg="white", bg="#2C3E50", font=("Helvetica", 10), cursor="hand2")
    lien1.pack(anchor="w", pady=2)

    lien2 = tk.Label(colonne3, text="👨‍🎓 Gestion Étudiants", fg="white", bg="#2C3E50", font=("Helvetica", 10), cursor="hand2")
    lien2.pack(anchor="w", pady=2)

    lien3 = tk.Label(colonne3, text="📘 Gestion Cours", fg="white", bg="#2C3E50", font=("Helvetica", 10), cursor="hand2")
    lien3.pack(anchor="w", pady=2)

    lien4 = tk.Label(colonne3, text="📝 Gestion Notes", fg="white", bg="#2C3E50", font=("Helvetica", 10), cursor="hand2")
    lien4.pack(anchor="w", pady=2)


    root.mainloop()


# Fonctions pour boutons (placeholder pour maintenant)
def ouvrir_gestion_etudiants():
    messagebox.showinfo("Gestion Étudiants", "Ouverture gestion des étudiants...")

def ouvrir_gestion_cours():
    messagebox.showinfo("Gestion Cours", "Ouverture gestion des cours...")

def ouvrir_gestion_notes():
    messagebox.showinfo("Gestion Notes", "Ouverture gestion des notes...")



if __name__ == "__main__":
    lancer_ui()