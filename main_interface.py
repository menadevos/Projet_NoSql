import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def ouvrir_gestion_etudiants():
    messagebox.showinfo("Gestion Étudiants", "Ouverture gestion des étudiants...")

def ouvrir_gestion_cours():
    messagebox.showinfo("Gestion Cours", "Ouverture gestion des cours...")

def ouvrir_gestion_notes():
    messagebox.showinfo("Gestion Notes", "Ouverture gestion des notes...")

def lancer_ui():
    root = tk.Tk()
    root.title("Application Gestion Étudiants")
    root.geometry("900x600")
    root.configure(bg="#F5F7FA")

    # ===== NAVBAR =====
    navbar = tk.Frame(root, bg="#2E1065", height=40)
    navbar.pack(fill="x")

    logo_img = Image.open("logo-white.png").resize((100, 50))
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(navbar, image=logo_photo, bg="#2E1065")
    logo_label.image = logo_photo
    logo_label.pack(side="left", padx=50, pady=10)

    right_frame = tk.Frame(navbar, bg="#2E1065")
    right_frame.pack(side="right", padx=30)

    phone_icon_img = Image.open("phone.png").resize((30, 20))
    phone_icon = ImageTk.PhotoImage(phone_icon_img)
    phone_label_icon = tk.Label(right_frame, image=phone_icon, bg="#2E1065")
    phone_label_icon.image = phone_icon
    phone_label_icon.pack(side="left", padx=(0, 5))

    phone_label = tk.Label(
        right_frame, text="+212 6 00 00 00 00", fg="white", bg="#2E1065",
        font=("Arial", 11, "bold"), cursor="hand2"
    )
    phone_label.pack(side="left", padx=(0, 25))

    email_icon_img = Image.open("email.png").resize((30, 20))
    email_icon = ImageTk.PhotoImage(email_icon_img)
    email_label_icon = tk.Label(right_frame, image=email_icon, bg="#2E1065")
    email_label_icon.image = email_icon
    email_label_icon.pack(side="left", padx=(0, 5))

    email_label = tk.Label(
        right_frame, text="contact@exemple.com", fg="white", bg="#2E1065",
        font=("Arial", 11, "bold"), cursor="hand2"
    )
    email_label.pack(side="left")

    def on_enter_email(e): email_label.config(fg="#FED600")
    def on_leave_email(e): email_label.config(fg="white")
    def on_enter_phone(e): phone_label.config(fg="#FED600")
    def on_leave_phone(e): phone_label.config(fg="white")

    email_label.bind("<Enter>", on_enter_email)
    email_label.bind("<Leave>", on_leave_email)
    phone_label.bind("<Enter>", on_enter_phone)
    phone_label.bind("<Leave>", on_leave_phone)

    # ===== LAYOUT PRINCIPAL =====
    layout_frame = tk.Frame(root, bg="#F5F7FA")
    layout_frame.pack(fill="both", expand=True)

    # ===== SIDEBAR =====
    sidebar = tk.Frame(layout_frame, bg="#2E1065", width=250)
    sidebar.pack(side="left", fill="y")

    sidebar_title = tk.Label(
        sidebar, bg="#2E1065", fg="white",
        font=("Helvetica", 16, "bold")
    )
    sidebar_title.pack(pady=20)

    # Fonction pour hover effect
    def on_enter_btn(e):
        e.widget.config(bg="#3F1A82")

    def on_leave_btn(e):
        e.widget.config(bg="#4B3C88")

    # Style des boutons
    btn_style = {
        "font": ("Helvetica", 14, "bold"),
        "bg": "#4B3C88",
        "fg": "white",
        "activebackground": "#3F1A82",
        "activeforeground": "white",
        "relief": "flat",
        "bd": 0,
        "width": 25,
        "height": 3,
        "cursor": "hand2"
    }

    btn1 = tk.Button(sidebar, text="👨‍🎓 Gestion des Étudiants", command=ouvrir_gestion_etudiants, **btn_style)
    btn1.pack(pady=10)
    btn1.bind("<Enter>", on_enter_btn)
    btn1.bind("<Leave>", on_leave_btn)

    btn2 = tk.Button(sidebar, text="📘 Gestion des Cours", command=ouvrir_gestion_cours, **btn_style)
    btn2.pack(pady=10)
    btn2.bind("<Enter>", on_enter_btn)
    btn2.bind("<Leave>", on_leave_btn)

    btn3 = tk.Button(sidebar, text="📝 Gestion des Notes", command=ouvrir_gestion_notes, **btn_style)
    btn3.pack(pady=10)
    btn3.bind("<Enter>", on_enter_btn)
    btn3.bind("<Leave>", on_leave_btn)

    # ===== CONTENU PRINCIPAL =====
    frame_contenu = tk.Frame(layout_frame, bg="#F5F7FA")
    frame_contenu.pack(side="left", fill="both", expand=True)

    titre = tk.Label(
        frame_contenu,
        text="Bienvenue dans l'application de gestion académique",
        font=("Helvetica", 20, "bold"),
        bg="#F5F7FA",
        fg="#2C3E50"
    )
    titre.pack(pady=30)

    root.mainloop()

if __name__ == "__main__":
    lancer_ui()
