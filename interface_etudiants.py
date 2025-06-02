# coding: utf-8
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from etudiants import ajouter_etudiant, lister_etudiants, supprimer_etudiant
from datetime import datetime
from uuid import UUID

etudiants_ids = []
selected_student_data = {}
all_students = []
student_widgets = []

def create_interface_etudiant(parent):
    container = tk.Frame(parent)
    manager = demarrer_interface(container)
    container.pack(fill="both", expand=True)
    return container


def demarrer_interface(parent=None):
    global etudiants_ids, selected_student_data, all_students, student_widgets

    # Determine root and container
    if parent is None:
        root = tk.Tk()
        root.title("Gestion des Étudiants - Interface Professionnelle")
        root.geometry("1000x750")
        root.configure(bg='#F8F6F0')  # vanilla_ice
        root.resizable(True, True)
        root.minsize(900, 650)
        container = root
    else:
        root = parent.winfo_toplevel()
        container = parent

    # Color palette
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

    # Configure styles
    style = ttk.Style()
    style.theme_use('clam')  # Use 'clam' theme for better customization

    style.configure('Title.TLabel',
                    background=colors['vanilla_ice'],
                    foreground=colors['text_dark'],
                    font=('Segoe UI', 22, 'bold'))

    style.configure('Subtitle.TLabel',
                    background=colors['vanilla_ice'],
                    foreground=colors['text_dark'],
                    font=('Segoe UI', 16, 'bold'))

    style.configure('Modern.TEntry',
                    fieldbackground=colors['accent'],
                    foreground=colors['text_dark'],
                    borderwidth=1)

    style.configure('Search.TEntry',
                    fieldbackground=colors['accent'],
                    foreground=colors['text_dark'],
                    borderwidth=2)

    # Main container - use the parent container directly
    main_container = container if parent is not None else tk.Frame(container, bg=colors['vanilla_ice'], relief='flat', bd=0)
    if parent is None:
        main_container.pack(fill='both', expand=True, padx=25, pady=25)

    content_frame = tk.Frame(main_container, bg=colors['vanilla_ice'])
    content_frame.pack(fill='both', expand=True)

    left_panel = tk.Frame(content_frame, bg=colors['vanilla_ice'], width=480)
    left_panel.pack(side='left', fill='both', expand=True, padx=(0, 15))
    left_panel.pack_propagate(False)

    right_panel = tk.Frame(content_frame, bg=colors['vanilla_ice'], width=480)
    right_panel.pack(side='right', fill='both', expand=True, padx=(15, 0))
    right_panel.pack_propagate(False)

    # Form section
    form_header = tk.Frame(left_panel, bg=colors['vanilla_ice'])
    form_header.pack(fill='x', pady=(0, 20))

    form_title = tk.Label(form_header, text="Informations de l'Étudiant",
                         bg=colors['vanilla_ice'], fg=colors['text_dark'],
                         font=('Segoe UI', 18, 'bold'))
    form_title.pack(side='left', padx=(10, 0))

    separator1 = tk.Frame(form_header, height=3, bg=colors['grape'])
    separator1.pack(fill='x', pady=(10, 0))

    form_container = tk.Frame(left_panel, bg=colors['accent'], relief='solid', bd=1)
    form_container.pack(fill='both', expand=True, pady=(10, 0))

    form_inner = tk.Frame(form_container, bg=colors['accent'])
    form_inner.pack(fill='both', expand=True, padx=20, pady=20)

    def create_form_field(parent, label_text, is_required=True, width=None):
        field_frame = tk.Frame(parent, bg=colors['accent'])
        field_frame.pack(fill='x', pady=(0, 15))

        label = tk.Label(field_frame,
                        text=label_text + (" *" if is_required else ""),
                        bg=colors['accent'], fg=colors['text_dark'],
                        font=('Segoe UI', 11, 'bold'))
        label.pack(anchor='w', pady=(0, 5))

        entry = ttk.Entry(field_frame, style='Modern.TEntry',
                         width=width if width else 40)
        entry.pack(fill='x' if not width else None, ipady=8)

        return entry

    row1 = tk.Frame(form_inner, bg=colors['accent'])
    row1.pack(fill='x', pady=(0, 15))

    nom_frame = tk.Frame(row1, bg=colors['accent'])
    nom_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
    entry_nom = create_form_field(nom_frame, "Nom")

    prenom_frame = tk.Frame(row1, bg=colors['accent'])
    prenom_frame.pack(side='right', fill='x', expand=True, padx=(10, 0))
    entry_prenom = create_form_field(prenom_frame, "Prénom")

    entry_email = create_form_field(form_inner, "Adresse Email")

    row3 = tk.Frame(form_inner, bg=colors['accent'])
    row3.pack(fill='x', pady=(0, 15))

    date_frame = tk.Frame(row3, bg=colors['accent'])
    date_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
    entry_date = create_form_field(date_frame, "Date de Naissance (YYYY-MM-DD)")

    id_frame = tk.Frame(row3, bg=colors['accent'])
    id_frame.pack(side='right', fill='x', expand=True, padx=(10, 0))
    id_label = tk.Label(id_frame, text="ID Étudiant", bg=colors['accent'],
                       fg=colors['text_dark'], font=('Segoe UI', 11, 'bold'))
    id_label.pack(anchor='w', pady=(0, 5))
    entry_id = ttk.Entry(id_frame, style='Modern.TEntry', state='readonly')
    entry_id.pack(fill='x', ipady=8)

    # Search section
    search_header = tk.Frame(right_panel, bg=colors['vanilla_ice'])
    search_header.pack(fill='x', pady=(0, 15))

    search_title = tk.Label(search_header, text="Recherche et Liste des Étudiants",
                           bg=colors['vanilla_ice'], fg=colors['text_dark'],
                           font=('Segoe UI', 18, 'bold'))
    search_title.pack(side='left', padx=(10, 0))

    separator2 = tk.Frame(search_header, height=3, bg=colors['light_grape'])
    separator2.pack(fill='x', pady=(10, 0))

    search_container = tk.Frame(right_panel, bg=colors['accent'], relief='solid', bd=1)
    search_container.pack(fill='x', pady=(10, 15))

    search_inner = tk.Frame(search_container, bg=colors['accent'])
    search_inner.pack(fill='x', padx=15, pady=12)

    search_label = tk.Label(search_inner, text=" Rechercher un étudiant:",
                           bg=colors['accent'], fg=colors['text_dark'],
                           font=('Segoe UI', 12, 'bold'))
    search_label.pack(anchor='w', pady=(0, 8))

    search_frame = tk.Frame(search_inner, bg=colors['accent'])
    search_frame.pack(fill='x')

    search_entry = ttk.Entry(search_frame, style='Search.TEntry')
    search_entry.pack(side='left', fill='x', expand=True, ipady=8, padx=(0, 10))

    clear_search_btn = tk.Button(search_frame, text="✕", bg=colors['danger'], fg=colors['vanilla_ice'],
                                font=('Arial', 10, 'bold'), bd=0, padx=8, pady=4,
                                command=lambda: clear_search())
    clear_search_btn.pack(side='right')

    list_container = tk.Frame(right_panel, bg=colors['accent'], relief='solid', bd=1)
    list_container.pack(fill='both', expand=True)

    list_header = tk.Frame(list_container, bg=colors['text_light'], height=35)
    list_header.pack(fill='x')
    list_header.pack_propagate(False)

    header_label = tk.Label(list_header, text=" Liste des Étudiants Inscrits",
                           bg=colors['text_light'], fg=colors['vanilla_ice'],
                           font=('Segoe UI', 12, 'bold'))
    header_label.pack(side='left', padx=15, pady=8)

    count_label = tk.Label(list_header, text="0 étudiant(s)",
                          bg=colors['text_light'], fg=colors['vanilla_ice'],
                          font=('Segoe UI', 10))
    count_label.pack(side='right', padx=15, pady=8)

    list_frame = tk.Frame(list_container, bg=colors['vanilla_ice'])
    list_frame.pack(fill='both', expand=True, padx=1, pady=1)

    scrollbar = tk.Scrollbar(list_frame, width=12, bg=colors['accent'],
                            troughcolor=colors['vanilla_ice'], activebackground=colors['grape'])
    scrollbar.pack(side='right', fill='y')

    list_canvas_frame = tk.Frame(list_frame, bg=colors['vanilla_ice'])
    list_canvas_frame.pack(side='left', fill='both', expand=True)

    separator3 = tk.Frame(left_panel, height=2, bg=colors['text_light'])
    separator3.pack(fill='x', pady=(20, 15))

    buttons_container = tk.Frame(left_panel, bg=colors['vanilla_ice'])
    buttons_container.pack(fill='x')

    buttons_row1 = tk.Frame(buttons_container, bg=colors['vanilla_ice'])
    buttons_row1.pack(fill='x', pady=(0, 10))

    buttons_row2 = tk.Frame(buttons_container, bg=colors['vanilla_ice'])
    buttons_row2.pack(fill='x')

    def create_modern_button(parent, text, bg_color, command, icon=""):
        btn = tk.Button(parent,
                       text=f"{icon} {text}" if icon else text,
                       bg=bg_color,
                       fg=colors['vanilla_ice'],
                       font=('Segoe UI', 11, 'bold'),
                       relief='flat',
                       bd=0,
                       padx=15,
                       pady=8,
                       cursor='hand2',
                       command=command)

        def on_enter(e):
            hover_colors = {
                colors['text_light']: '#5a6268',
                colors['provincial']: '#138496',
                colors['success']: '#0e8c6b',
                colors['danger']: '#c82333',
                colors['grape']: '#6d28d9',
                colors['warning']: '#d97706'
            }
            btn.config(bg=hover_colors.get(bg_color, bg_color))

        def on_leave(e):
            btn.config(bg=bg_color)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    btn_annuler = create_modern_button(buttons_row1, "Annuler", colors['text_light'],
                                      lambda: clear_form(), "")
    btn_annuler.pack(side='left', padx=(0, 8))

    btn_reinitialiser = create_modern_button(buttons_row1, "Réinitialiser", colors['provincial'],
                                           lambda: clear_form(), "")
    btn_reinitialiser.pack(side='left', padx=4)

    btn_enregistrer = create_modern_button(buttons_row1, "Enregistrer", colors['success'],
                                         lambda: ajouter_etudiant_ui(), "")
    btn_enregistrer.pack(side='right', padx=(8, 0))

    btn_supprimer = create_modern_button(buttons_row2, "Supprimer Sélectionné", colors['danger'],
                                       lambda: supprimer_etudiant_ui(), "")
    btn_supprimer.pack(side='left', padx=(0, 8))

    btn_voir_details = create_modern_button(buttons_row2, "Charger Détails", colors['grape'],
                                          lambda: voir_details(), "")
    btn_voir_details.pack(side='right', padx=(8, 0))

    help_container = tk.Frame(main_container, bg=colors['accent'], relief='solid', bd=1)
    help_container.pack(fill='x', pady=(25, 0))

    help_inner = tk.Frame(help_container, bg=colors['accent'])
    help_inner.pack(fill='x', padx=20, pady=12)

    help_text = tk.Label(help_inner,
                        text="Les champs marqués (*) sont obligatoires • Double-clic pour charger • Utilisez la recherche pour filtrer",
                        bg=colors['accent'], fg=colors['text_dark'],
                        font=('Segoe UI', 10))
    help_text.pack(side='left')

    def clear_form():
        entry_nom.delete(0, tk.END)
        entry_prenom.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_date.delete(0, tk.END)
        entry_id.configure(state='normal')
        entry_id.delete(0, tk.END)
        entry_id.configure(state='readonly')
        selected_student_data.clear()

    def load_student_to_form(etudiant):
        clear_form()
        entry_nom.insert(0, etudiant.nom)
        entry_prenom.insert(0, etudiant.prenom)
        entry_email.insert(0, etudiant.email)
        entry_date.insert(0, str(etudiant.date_naissance))
        entry_id.configure(state='normal')
        entry_id.insert(0, str(etudiant.id))
        entry_id.configure(state='readonly')
        selected_student_data['id'] = etudiant.id

    def create_student_widget(parent, etudiant, index):
        student_frame = tk.Frame(parent, bg=colors['vanilla_ice'], relief='solid', bd=1)
        student_frame.pack(fill='x', padx=5, pady=2)

        bg_color = colors['accent'] if index % 2 == 0 else colors['vanilla_ice']
        student_frame.config(bg=bg_color)

        content_frame = tk.Frame(student_frame, bg=bg_color)
        content_frame.pack(side='left', fill='both', expand=True, padx=10, pady=8)

        main_info = tk.Label(content_frame,
                            text=f"👤 {etudiant.nom} {etudiant.prenom}",
                            bg=bg_color, fg=colors['text_dark'],
                            font=('Segoe UI', 11, 'bold'))
        main_info.pack(anchor='w')

        secondary_info = tk.Label(content_frame,
                                 text=f"✉️ {etudiant.email} | 📅 ID: {etudiant.id}",
                                 bg=bg_color, fg=colors['text_light'],
                                 font=('Segoe UI', 9))
        secondary_info.pack(anchor='w', pady=(2, 0))

        actions_frame = tk.Frame(student_frame, bg=bg_color)
        actions_frame.pack(side='right', padx=10, pady=5)

        delete_btn = tk.Button(actions_frame, text="Supprimer", bg=colors['danger'], fg=colors['vanilla_ice'],
                              font=('Arial', 10, 'bold'), bd=0, padx=8, pady=4,
                              command=lambda: supprimer_etudiant_individuel(etudiant.id))
        delete_btn.pack(side='right', padx=2)

        details_btn = tk.Button(actions_frame, text="Modifier", bg=colors['grape'], fg=colors['vanilla_ice'],
                               font=('Arial', 10, 'bold'), bd=0, padx=8, pady=4,
                               command=lambda: load_student_to_form(etudiant))
        details_btn.pack(side='right', padx=2)

        def on_hover_enter(e):
            student_frame.config(bg=colors['light_grape'], bd=2)
            content_frame.config(bg=colors['light_grape'])
            actions_frame.config(bg=colors['light_grape'])
            main_info.config(bg=colors['light_grape'])
            secondary_info.config(bg=colors['light_grape'])

        def on_hover_leave(e):
            student_frame.config(bg=bg_color, bd=1)
            content_frame.config(bg=bg_color)
            actions_frame.config(bg=bg_color)
            main_info.config(bg=bg_color)
            secondary_info.config(bg=bg_color)

        student_frame.bind("<Enter>", on_hover_enter)
        student_frame.bind("<Leave>", on_hover_leave)
        content_frame.bind("<Enter>", on_hover_enter)
        content_frame.bind("<Leave>", on_hover_leave)

        def on_double_click(e):
            load_student_to_form(etudiant)
            messagebox.showinfo("Information", "Étudiant chargé dans le formulaire")

        student_frame.bind("<Double-Button-1>", on_double_click)
        content_frame.bind("<Double-Button-1>", on_double_click)

        return student_frame

    def afficher_etudiants(filter_text=""):
        global etudiants_ids, all_students, student_widgets

        for widget in student_widgets:
            widget.destroy()
        student_widgets = []

        etudiants_ids = []
        all_students = list(lister_etudiants())

        if filter_text:
            filtered_students = [
                etudiant for etudiant in all_students
                if filter_text.lower() in f"{etudiant.nom} {etudiant.prenom} {etudiant.email}".lower()
            ]
            students_to_show = filtered_students
        else:
            students_to_show = all_students

        for index, etudiant in enumerate(students_to_show):
            widget = create_student_widget(list_canvas_frame, etudiant, index)
            student_widgets.append(widget)
            etudiants_ids.append(etudiant.id)

        count_label.config(text=f"{len(students_to_show)} étudiant(s)")

        if not students_to_show:
            no_result_frame = tk.Frame(list_canvas_frame, bg=colors['vanilla_ice'])
            no_result_frame.pack(fill='both', expand=True, pady=50)

            no_result_label = tk.Label(no_result_frame,
                                     text="🔍 Aucun étudiant trouvé" if filter_text else "📝 Aucun étudiant enregistré",
                                     bg=colors['vanilla_ice'], fg=colors['text_light'],
                                     font=('Segoe UI', 14))
            no_result_label.pack()

            student_widgets.append(no_result_frame)

    def rechercher_etudiants():
        filter_text = search_entry.get().strip()
        afficher_etudiants(filter_text) # Pass the filter text to the afficher_etudiants function

    def clear_search():
        search_entry.delete(0, tk.END)
        afficher_etudiants()

    def ajouter_etudiant_ui():
        global student_widgets
        nom = entry_nom.get().strip()
        prenom = entry_prenom.get().strip()
        email = entry_email.get().strip()
        date_naissance_str = entry_date.get().strip()

        if not nom or not prenom or not email or not date_naissance_str:
            messagebox.showwarning("❌ Erreur de Validation",
                                 "Tous les champs marqués (*) sont obligatoires")
            return

        try:
            # Convert date string to datetime.date
            date_naissance = datetime.strptime(date_naissance_str, '%Y-%m-%d').date()
            ajouter_etudiant(nom, prenom, email, date_naissance)
            messagebox.showinfo("✅ Succès", "Étudiant ajouté avec succès!")
            clear_form()
            afficher_etudiants()
            clear_search()
        except ValueError:
            messagebox.showerror("❌ Erreur", "Format de date invalide. Utilisez YYYY-MM-DD.")
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Impossible d'ajouter l'étudiant:\n{str(e)}")

    def supprimer_etudiant_individuel(etudiant_id: UUID):
        global student_widgets
        try:
            result = messagebox.askyesno("⚠️ Confirmation",
                                       "Êtes-vous sûr de vouloir supprimer cet étudiant?\n\nCette action est irréversible.")
            if result:
                supprimer_etudiant(etudiant_id)
                messagebox.showinfo("✅ Succès", "Étudiant supprimé avec succès!")
                clear_form()
                afficher_etudiants()
                clear_search()
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Impossible de supprimer l'étudiant:\n{str(e)}")

    def supprimer_etudiant_ui():
        if not selected_student_data.get('id'):
            messagebox.showwarning("⚠️ Sélection Requise",
                                 "Veuillez d'abord charger un étudiant dans le formulaire")
            return

        supprimer_etudiant_individuel(selected_student_data['id'])

    def voir_details():
        if not student_widgets or not all_students:
            messagebox.showinfo("ℹ️ Information", "Aucun étudiant disponible")
            return

        messagebox.showinfo("ℹ️ Information",
                          "Double-cliquez sur un étudiant dans la liste pour charger ses détails")

    search_entry.bind('<KeyRelease>', lambda e: rechercher_etudiants())

    if parent is None:
        root.bind('<Control-n>', lambda e: clear_form())
        root.bind('<Control-s>', lambda e: ajouter_etudiant_ui())
        root.bind('<Control-f>', lambda e: search_entry.focus())
        root.bind('<Escape>', lambda e: clear_search())

    afficher_etudiants()

    if parent is None:
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (root.winfo_screenheight() // 2) - (750 // 2)
        root.geometry(f'1000x750+{x}+{y}')
        entry_nom.focus()
        root.mainloop()

    return container

if __name__ == "__main__":
    demarrer_interface()