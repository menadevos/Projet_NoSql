import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from Interface_cour import create_interface_cours  # Interface 1
from gestion_notes import create_note_interface   # Interface 2


def lancer_ui():
    root = tk.Tk()
    root.title("Application Gestion Étudiants")
    root.geometry("900x600")
    root.configure(bg="#F5F7FA")
    colors = {
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
    # ===== NAVBAR =====
    navbar = tk.Frame(root, bg="#2E1065", height=50)
    navbar.pack(fill="x")

    logo_img = Image.open("logo-white.png").resize((120, 60))
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(navbar, image=logo_photo, bg="#2E1065")
    logo_label.image = logo_photo
    logo_label.pack(side="left", padx=50, pady=10)

      # Titre principal avec style moderne
    title_label = tk.Label(navbar, text=" GESTION DES NOTES ÉTUDIANTS",
                              font=('Segoe UI', 18, 'bold'),
                              fg='white', bg=colors['cosmic'])
    title_label.pack( expand=True)
    title_label.place(relx=0.5, rely=0.5, anchor='center')
        
    

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


  
    # ===== Conteneur principal dynamique =====
    content_frame = tk.Frame(root, bg="#F5F7FA")
    content_frame.pack(fill="both", expand=True)


    # ===== Fonctions pour afficher les interfaces =====
    def ouvrir_interface_1():
        for widget in content_frame.winfo_children():
            widget.destroy()

        main_container = tk.Frame(content_frame, bg="#F5F7FA")
        main_container.pack(fill="both", expand=True)

        btn_retour = tk.Button(main_container,
                       text="←",
                       bg="#EF4444",
                       fg="white",
                       font=("Arial", 12, "bold"),
                       width=2,  # largeur du bouton
                       height=1,  # hauteur du bouton
                       bd=0,
                       relief="flat",
                       command=afficher_boutons,
                       cursor="hand2"  
                       )
        btn_retour.pack(anchor="nw", padx=10, pady=10)

        frame_cours = create_interface_cours(main_container)
        if frame_cours:
            frame_cours.pack(fill="both", expand=True)

    def ouvrir_interface_2():
        for widget in content_frame.winfo_children():
            widget.destroy()

        main_container = tk.Frame(content_frame, bg="#F5F7FA")
        main_container.pack(fill="both", expand=True)

        btn_retour = tk.Button(main_container,
                       text="←",
                       bg="#EF4444",
                       fg="white",
                       font=("Arial", 12, "bold"),
                       width=2,  # largeur du bouton
                       height=1,  # hauteur du bouton
                       bd=0,
                       relief="flat",
                       command=afficher_boutons,
                       cursor="hand2"  
                       )
        btn_retour.pack(anchor="nw", padx=10, pady=10)

        frame_note = create_note_interface(main_container)
        if frame_note:
            frame_note.pack(fill="both", expand=True)

        
    
    def ouvrir_interface_4():
        for widget in content_frame.winfo_children():
            widget.destroy()

        main_container = tk.Frame(content_frame, bg="#F5F7FA")
        main_container.pack(fill="both", expand=True)

        btn_retour = tk.Button(main_container,
                       text="←",
                       bg="#EF4444",
                       fg="white",
                       font=("Arial", 12, "bold"),
                       width=2,  # largeur du bouton
                       height=1,  # hauteur du bouton
                       bd=0,
                       relief="flat",
                       command=afficher_boutons,
                       cursor="hand2"  
                       )
        btn_retour.pack(anchor="nw", padx=10, pady=10)

        frame_note = create_stats_interface(main_container)
        if frame_note:
            frame_note.pack(fill="both", expand=True)



    def ouvrir_interface_3():
        messagebox.showinfo("Action", "Ouverture Interface 3")

    def afficher_boutons():
        # Supprime tout dans content_frame
        for widget in content_frame.winfo_children():
            widget.destroy()

        # Création d'un canvas pour fond dégradé (optionnel)
        canvas = tk.Canvas(content_frame, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        def draw_gradient(canvas, width, height, color1, color2):
            steps = 100
            r1, g1, b1 = root.winfo_rgb(color1)
            r2, g2, b2 = root.winfo_rgb(color2)
            r_ratio = (r2 - r1) / steps
            g_ratio = (g2 - g1) / steps
            b_ratio = (b2 - b1) / steps

            for i in range(steps):
                nr = int(r1 + (r_ratio * i))
                ng = int(g1 + (g_ratio * i))
                nb = int(b1 + (b_ratio * i))
                color = f'#{nr >> 8:02x}{ng >> 8:02x}{nb >> 8:02x}'
                y1 = int(i * height / steps)
                y2 = int((i + 1) * height / steps)
                canvas.create_rectangle(0, y1, width, y2, outline="", fill=color)

        # Données boutons (texte + icône fichier + fonction clic)
        buttons_data = [
            ("Gestion des cours", "cours.png", ouvrir_interface_1),
            ("Gestion des notes", "notes.png", ouvrir_interface_2),
            ("Gestion des étudiants", "students.png", ouvrir_interface_3),
            ("Statistiques", "stats.png", ouvrir_interface_4), 
        ]

        # Chargement images icônes (doivent être dans le dossier)
        icons = {}
        for text, icon_file, cmd in buttons_data:
            try:
                img = Image.open(icon_file).resize((100, 100))
                icons[text] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Erreur chargement icône {icon_file}: {e}")
                icons[text] = None

        card_width = 600
        card_height = 170
        card_bg = "#F3F4F6"
        card_hover_bg = "#4B3C88"
        card_fg = "#333"
        card_font = ("Segoe UI", 20, "bold")

        cards = []
        card_windows = []  # Pour stocker les références des fenêtres canvas
        cards_created = False

        def make_card(parent, text, icon, command, card_index):
            frame = tk.Frame(parent, width=card_width, height=card_height, bg=card_bg, relief="raised", bd=2, cursor="hand2")
            frame.pack_propagate(False)  # Empêche le redimensionnement automatique

            icon_label = None
            # Icône à gauche
            if icon:
                icon_label = tk.Label(frame, image=icon, bg=card_bg)
                icon_label.image = icon
                icon_label.pack(side="left", padx=20, pady=20)

            # Texte à droite, centré verticalement
            text_label = tk.Label(frame, text=text, bg=card_bg, fg=card_fg, font=card_font)
            text_label.pack(side="left", padx=30, pady=20, fill="both", expand=True)

            # Variables pour l'animation
            original_x = [50]  # Position originale à gauche avec marge

            # Effets survol avec mouvement
            def on_enter(e):
                frame.config(bg=card_hover_bg)
                if icon_label:
                    icon_label.config(bg=card_hover_bg)
                text_label.config(bg=card_hover_bg)
                
                # Déplacer la carte vers la droite si elle existe dans le canvas
                if card_index < len(card_windows) and card_windows[card_index]:
                    coords = canvas.coords(card_windows[card_index])
                    if len(coords) >= 2:
                        canvas.coords(card_windows[card_index], original_x[0] + 30, coords[1])

            def on_leave(e):
                frame.config(bg=card_bg)
                if icon_label:
                    icon_label.config(bg=card_bg)
                text_label.config(bg=card_bg)
                
                # Remettre la carte à sa position originale
                if card_index < len(card_windows) and card_windows[card_index]:
                    coords = canvas.coords(card_windows[card_index])
                    if len(coords) >= 2:
                        canvas.coords(card_windows[card_index], original_x[0], coords[1])

            frame.bind("<Enter>", on_enter)
            frame.bind("<Leave>", on_leave)
            text_label.bind("<Enter>", on_enter)
            text_label.bind("<Leave>", on_leave)
            if icon_label:
                icon_label.bind("<Enter>", on_enter)
                icon_label.bind("<Leave>", on_leave)

            # Clic sur la card
            frame.bind("<Button-1>", lambda e: command())
            text_label.bind("<Button-1>", lambda e: command())
            if icon_label:
                icon_label.bind("<Button-1>", lambda e: command())

            return frame

        def create_cards():
            nonlocal cards_created
            if not cards_created:
                for i, (text, icon_file, cmd) in enumerate(buttons_data):
                    card = make_card(canvas, text, icons.get(text), cmd, i)
                    cards.append(card)
                cards_created = True

        def redraw(event):
            canvas.delete("all")
            w = event.width
            h = event.height
            draw_gradient(canvas, w, h, "#667eea", "#764ba2")
            place_buttons()

        def place_buttons():
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            
            # Créer les cartes si elles n'existent pas encore
            create_cards()
            
            # Calculer la position pour aligner à gauche avec marge
            left_margin = 50  # Marge à gauche
            
            # Calculer la position verticale pour centrer les cartes
            total_height = len(cards) * (card_height + 40)  # hauteur + padding
            start_y = max(50, (canvas_height - total_height) // 2)
            
            # Supprimer les anciennes fenêtres et en créer de nouvelles
            card_windows.clear()
            for i, card in enumerate(cards):
                y_position = start_y + i * (card_height + 40)
                window = canvas.create_window(left_margin, y_position, window=card, anchor="nw")
                card_windows.append(window)

        canvas.bind("<Configure>", redraw)

    # Affiche le menu initial
    afficher_boutons()

    root.mainloop()


if __name__ == "__main__":
    lancer_ui()