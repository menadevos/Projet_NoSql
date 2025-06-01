# coding: utf-8
import Tkinter as tk
import tkMessageBox as messagebox
import ttk
from etudiants import ajouter_etudiant, lister_etudiants, supprimer_etudiant

etudiants_ids = []
selected_student_data = {}
all_students = []
student_widgets = []

def demarrer_interface():
    global etudiants_ids, selected_student_data, all_students, student_widgets
    
    root = tk.Tk()
    root.title("Gestion des Étudiants - Interface Professionnelle")
    root.geometry("1000x750")
    root.configure(bg='#f8f9fa')
    root.resizable(True, True)
    root.minsize(900, 650)
    
    style = ttk.Style()
    style.theme_use('clam')
    
    style.configure('Title.TLabel', 
                   background='#f8f9fa', 
                   foreground='#2c3e50', 
                   font=('Segoe UI', 22, 'bold'))
    
    style.configure('Subtitle.TLabel', 
                   background='#f8f9fa', 
                   foreground='#2c3e50', 
                   font=('Segoe UI', 16, 'bold'))
    
    style.configure('Modern.TEntry',
                   fieldbackground='#ffffff',
                   borderwidth=1,
                   relief='solid',
                   focuscolor='#007bff')
    
    style.configure('Search.TEntry',
                   fieldbackground='#f8f9fa',
                   borderwidth=2,
                   relief='solid',
                   focuscolor='#28a745')
    
    title_frame = tk.Frame(root, bg='#2c3e50', height=60)
    title_frame.pack(fill='x')
    title_frame.pack_propagate(False)
    
    gradient_frame1 = tk.Frame(title_frame, bg='#34495e', height=15)
    gradient_frame1.pack(fill='x')
    gradient_frame2 = tk.Frame(title_frame, bg='#2c3e50', height=30)
    gradient_frame2.pack(fill='x')
    gradient_frame3 = tk.Frame(title_frame, bg='#1a252f', height=15)
    gradient_frame3.pack(fill='x')
    
    title_content = tk.Frame(gradient_frame2, bg='#2c3e50')
    title_content.pack(expand=True, fill='both')
    
    title_icon = tk.Label(title_content, text="", bg='#2c3e50', fg='white', font=('Arial', 20))
    title_icon.pack(side='left', padx=(20, 10), pady=5)
    
    title_label = tk.Label(title_content, 
                          text="Système de Gestion des Étudiants",
                          bg='#2c3e50', 
                          fg='white',
                          font=('Segoe UI', 18, 'bold'))
    title_label.pack(side='left', pady=5)
    
    controls_frame = tk.Frame(title_content, bg='#2c3e50')
    controls_frame.pack(side='right', padx=15, pady=5)
    
    minimize_btn = tk.Button(controls_frame, text="—", bg='#f39c12', fg='white',
                            font=('Arial', 10, 'bold'), bd=0, width=3, height=1,
                            command=lambda: root.iconify())
    minimize_btn.pack(side='left', padx=2)
    
    close_btn = tk.Button(controls_frame, text="×", bg='#e74c3c', fg='white',
                         font=('Arial', 12, 'bold'), bd=0, width=3, height=1,
                         command=root.quit)
    close_btn.pack(side='left', padx=2)
    
    shadow_frame = tk.Frame(root, bg='#bdc3c7', height=2)
    shadow_frame.pack(fill='x')
    
    main_container = tk.Frame(root, bg='white', relief='flat', bd=0)
    main_container.pack(fill='both', expand=True, padx=25, pady=25)
    
    content_frame = tk.Frame(main_container, bg='white')
    content_frame.pack(fill='both', expand=True)
    
    left_panel = tk.Frame(content_frame, bg='white', width=480)
    left_panel.pack(side='left', fill='both', expand=True, padx=(0, 15))
    left_panel.pack_propagate(False)
    
    right_panel = tk.Frame(content_frame, bg='white', width=480)
    right_panel.pack(side='right', fill='both', expand=True, padx=(15, 0))
    right_panel.pack_propagate(False)
    
    form_header = tk.Frame(left_panel, bg='white')
    form_header.pack(fill='x', pady=(0, 20))
    
    form_icon = tk.Label(form_header, text="", bg='white', font=('Arial', 24))
    form_icon.pack(side='left')
    
    form_title = tk.Label(form_header, text="Informations de l'Étudiant",
                         bg='white', fg='#2c3e50', font=('Segoe UI', 18, 'bold'))
    form_title.pack(side='left', padx=(10, 0))
    
    separator1 = tk.Frame(form_header, height=3, bg='#3498db')
    separator1.pack(fill='x', pady=(10, 0))
    
    form_container = tk.Frame(left_panel, bg='#f8f9fa', relief='solid', bd=1)
    form_container.pack(fill='both', expand=True, pady=(10, 0))
    
    form_inner = tk.Frame(form_container, bg='#f8f9fa')
    form_inner.pack(fill='both', expand=True, padx=20, pady=20)
    
    def create_form_field(parent, label_text, is_required=True, width=None):
        field_frame = tk.Frame(parent, bg='#f8f9fa')
        field_frame.pack(fill='x', pady=(0, 15))
        
        label = tk.Label(field_frame, 
                        text=label_text + (" *" if is_required else ""),
                        bg='#f8f9fa', fg='#495057', 
                        font=('Segoe UI', 11, 'bold'))
        label.pack(anchor='w', pady=(0, 5))
        
        entry = tk.Entry(field_frame, 
                        font=('Segoe UI', 11), 
                        bg='white', 
                        relief='solid', 
                        bd=1,
                        width=width if width else 40)
        entry.pack(fill='x' if not width else None, ipady=8)
        
        def on_focus_in(event):
            event.widget.config(bg='#e3f2fd', relief='solid', bd=2)
        def on_focus_out(event):
            event.widget.config(bg='white', relief='solid', bd=1)
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        return entry
    
    row1 = tk.Frame(form_inner, bg='#f8f9fa')
    row1.pack(fill='x', pady=(0, 15))
    
    nom_frame = tk.Frame(row1, bg='#f8f9fa')
    nom_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
    entry_nom = create_form_field(nom_frame, "Nom")
    
    prenom_frame = tk.Frame(row1, bg='#f8f9fa')
    prenom_frame.pack(side='right', fill='x', expand=True, padx=(10, 0))
    entry_prenom = create_form_field(prenom_frame, "Prénom")
    
    entry_email = create_form_field(form_inner, "Adresse Email")
    
    row3 = tk.Frame(form_inner, bg='#f8f9fa')
    row3.pack(fill='x', pady=(0, 15))
    
    date_frame = tk.Frame(row3, bg='#f8f9fa')
    date_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
    entry_date = create_form_field(date_frame, "Date de Naissance")
    
    id_frame = tk.Frame(row3, bg='#f8f9fa')
    id_frame.pack(side='right', fill='x', expand=True, padx=(10, 0))
    id_label = tk.Label(id_frame, text="ID Étudiant", bg='#f8f9fa', fg='#495057', 
                       font=('Segoe UI', 11, 'bold'))
    id_label.pack(anchor='w', pady=(0, 5))
    entry_id = tk.Entry(id_frame, font=('Segoe UI', 11), bg='#e9ecef', 
                       relief='solid', bd=1, state='readonly')
    entry_id.pack(fill='x', ipady=8)
    
    search_header = tk.Frame(right_panel, bg='white')
    search_header.pack(fill='x', pady=(0, 15))
    
    search_icon = tk.Label(search_header, text="", bg='white', font=('Arial', 24))
    search_icon.pack(side='left')
    
    search_title = tk.Label(search_header, text="Recherche et Liste des Étudiants",
                           bg='white', fg='#2c3e50', font=('Segoe UI', 18, 'bold'))
    search_title.pack(side='left', padx=(10, 0))
    
    separator2 = tk.Frame(search_header, height=3, bg='#28a745')
    separator2.pack(fill='x', pady=(10, 0))
    
    search_container = tk.Frame(right_panel, bg='#e8f5e8', relief='solid', bd=1)
    search_container.pack(fill='x', pady=(10, 15))
    
    search_inner = tk.Frame(search_container, bg='#e8f5e8')
    search_inner.pack(fill='x', padx=15, pady=12)
    
    search_label = tk.Label(search_inner, text=" Rechercher un étudiant:",
                           bg='#e8f5e8', fg='#155724', font=('Segoe UI', 12, 'bold'))
    search_label.pack(anchor='w', pady=(0, 8))
    
    search_frame = tk.Frame(search_inner, bg='#e8f5e8')
    search_frame.pack(fill='x')
    
    search_entry = tk.Entry(search_frame, font=('Segoe UI', 12), bg='white',
                           relief='solid', bd=2, fg='#495057')
    search_entry.pack(side='left', fill='x', expand=True, ipady=8, padx=(0, 10))
    
    clear_search_btn = tk.Button(search_frame, text="✕", bg='#dc3545', fg='white',
                                font=('Arial', 10, 'bold'), bd=0, padx=8, pady=4,
                                command=lambda: clear_search())
    clear_search_btn.pack(side='right')
    
    list_container = tk.Frame(right_panel, bg='#f8f9fa', relief='solid', bd=1)
    list_container.pack(fill='both', expand=True)
    
    list_header = tk.Frame(list_container, bg='#6c757d', height=35)
    list_header.pack(fill='x')
    list_header.pack_propagate(False)
    
    header_label = tk.Label(list_header, text=" Liste des Étudiants Inscrits",
                           bg='#6c757d', fg='white', font=('Segoe UI', 12, 'bold'))
    header_label.pack(side='left', padx=15, pady=8)
    
    count_label = tk.Label(list_header, text="0 étudiant(s)",
                          bg='#6c757d', fg='#ffffff', font=('Segoe UI', 10))
    count_label.pack(side='right', padx=15, pady=8)
    
    list_frame = tk.Frame(list_container, bg='white')
    list_frame.pack(fill='both', expand=True, padx=1, pady=1)
    
    scrollbar = tk.Scrollbar(list_frame, width=12, bg='#e9ecef', 
                            troughcolor='#f8f9fa', activebackground='#007bff')
    scrollbar.pack(side='right', fill='y')
    
    list_canvas_frame = tk.Frame(list_frame, bg='white')
    list_canvas_frame.pack(side='left', fill='both', expand=True)
    
    separator3 = tk.Frame(left_panel, height=2, bg='#dee2e6')
    separator3.pack(fill='x', pady=(20, 15))
    
    buttons_container = tk.Frame(left_panel, bg='white')
    buttons_container.pack(fill='x')
    
    buttons_row1 = tk.Frame(buttons_container, bg='white')
    buttons_row1.pack(fill='x', pady=(0, 10))
    
    buttons_row2 = tk.Frame(buttons_container, bg='white')
    buttons_row2.pack(fill='x')
    
    def create_modern_button(parent, text, bg_color, command, icon=""):
        btn = tk.Button(parent, 
                       text = "{} {}".format(icon, text) if icon else text,
                       bg=bg_color, 
                       fg='white',
                       font=('Segoe UI', 11, 'bold'),
                       relief='flat',
                       bd=0,
                       padx=15,
                       pady=8,
                       cursor='hand2',
                       command=command)
        
        def on_enter(e):
            hover_colors = {
                '#6c757d': '#5a6268',
                '#17a2b8': '#138496', 
                '#28a745': '#218838',
                '#dc3545': '#c82333',
                '#007bff': '#0056b3',
                '#ffc107': '#e0a800'
            }
            btn.config(bg=hover_colors.get(bg_color, bg_color))
        
        def on_leave(e):
            btn.config(bg=bg_color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    btn_annuler = create_modern_button(buttons_row1, "Annuler", '#6c757d', 
                                      lambda: clear_form(), "")
    btn_annuler.pack(side='left', padx=(0, 8))
    
    btn_reinitialiser = create_modern_button(buttons_row1, "Réinitialiser", '#17a2b8',
                                           lambda: clear_form(), "")
    btn_reinitialiser.pack(side='left', padx=4)
    
    btn_enregistrer = create_modern_button(buttons_row1, "Enregistrer", '#28a745',
                                         lambda: ajouter_etudiant_ui(), "")
    btn_enregistrer.pack(side='right', padx=(8, 0))
    
    btn_supprimer = create_modern_button(buttons_row2, "Supprimer Sélectionné", '#dc3545',
                                       lambda: supprimer_etudiant_ui(), "")
    btn_supprimer.pack(side='left', padx=(0, 8))
    
    btn_voir_details = create_modern_button(buttons_row2, "Charger Détails", '#007bff',
                                          lambda: voir_details(), "")
    btn_voir_details.pack(side='right', padx=(8, 0))
    
    help_container = tk.Frame(main_container, bg='#d1ecf1', relief='solid', bd=1)
    help_container.pack(fill='x', pady=(25, 0))
    
    help_inner = tk.Frame(help_container, bg='#d1ecf1')
    help_inner.pack(fill='x', padx=20, pady=12)
    
    help_icon = tk.Label(help_inner, text="", bg='#d1ecf1', font=('Arial', 16))
    help_icon.pack(side='left', padx=(0, 10))
    
    help_text = tk.Label(help_inner,
                        text="Les champs marqués (*) sont obligatoires • Double-clic pour charger • Utilisez la recherche pour filtrer",
                        bg='#d1ecf1', fg='#0c5460', font=('Segoe UI', 10))
    help_text.pack(side='left')
    
    def clear_form():
        entry_nom.delete(0, tk.END)
        entry_prenom.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_date.delete(0, tk.END)
        entry_id.config(state='normal')
        entry_id.delete(0, tk.END)
        entry_id.config(state='readonly')
        selected_student_data.clear()
    
    def load_student_to_form(etudiant):
        clear_form()
        entry_nom.insert(0, etudiant.nom)
        entry_prenom.insert(0, etudiant.prenom)
        entry_email.insert(0, etudiant.email)
        entry_date.insert(0, str(etudiant.date_naissance))
        entry_id.config(state='normal')
        entry_id.insert(0, str(etudiant.id))
        entry_id.config(state='readonly')
        selected_student_data['id'] = etudiant.id
    
    def create_student_widget(parent, etudiant, index):
        student_frame = tk.Frame(parent, bg='white', relief='solid', bd=1)
        student_frame.pack(fill='x', padx=5, pady=2)
        
        bg_color = '#f8f9fa' if index % 2 == 0 else 'white'
        student_frame.config(bg=bg_color)
        
        content_frame = tk.Frame(student_frame, bg=bg_color)
        content_frame.pack(side='left', fill='both', expand=True, padx=10, pady=8)
        
        main_info = tk.Label(content_frame,
                            text = u"👤 {} {}".format(etudiant.nom, etudiant.prenom),
                            bg=bg_color, fg='#2c3e50',
                            font=('Segoe UI', 11, 'bold'))
        main_info.pack(anchor='w')
        
        secondary_info = tk.Label(content_frame,
                                 text = u"✉️ {} | 📅 ID: {}".format(etudiant.email, etudiant.id),
                                 bg=bg_color, fg='#6c757d',
                                 font=('Segoe UI', 9))
        secondary_info.pack(anchor='w', pady=(2, 0))
        
        actions_frame = tk.Frame(student_frame, bg=bg_color)
        actions_frame.pack(side='right', padx=10, pady=5)
        
        delete_btn = tk.Button(actions_frame, text="Supprimer", bg='#dc3545', fg='white',
                              font=('Arial', 10, 'bold'), bd=0, padx=8, pady=4,
                              command=lambda: supprimer_etudiant_individuel(etudiant.id))
        delete_btn.pack(side='right', padx=2)
        
        details_btn = tk.Button(actions_frame, text="modifier", bg='#007bff', fg='white',
                               font=('Arial', 10, 'bold'), bd=0, padx=8, pady=4,
                               command=lambda: load_student_to_form(etudiant))
        details_btn.pack(side='right', padx=2)
        
        def on_hover_enter(e):
            student_frame.config(bg='#e3f2fd', bd=2)
            content_frame.config(bg='#e3f2fd')
            actions_frame.config(bg='#e3f2fd')
            main_info.config(bg='#e3f2fd')
            secondary_info.config(bg='#e3f2fd')
        
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
            filtered_students = []
            for etudiant in all_students:
                search_text = (u"{} {} {}".format(etudiant.nom, etudiant.prenom, etudiant.email)).lower()
                if filter_text.lower() in search_text:
                    filtered_students.append(etudiant)
            students_to_show = filtered_students
        else:
            students_to_show = all_students
        
        for index, etudiant in enumerate(students_to_show):
            widget = create_student_widget(list_canvas_frame, etudiant, index)
            student_widgets.append(widget)
            etudiants_ids.append(etudiant.id)
        
        count_label.config(text=u"{} étudiant(s)".format(len(students_to_show)))
        
        if not students_to_show:
            no_result_frame = tk.Frame(list_canvas_frame, bg='white')
            no_result_frame.pack(fill='both', expand=True, pady=50)
            
            no_result_label = tk.Label(no_result_frame,
                                      text="🔍 Aucun étudiant trouvé" if filter_text else "📝 Aucun étudiant enregistré",
                                      bg='white', fg='#6c757d',
                                      font=('Segoe UI', 14))
            no_result_label.pack()
            
            student_widgets.append(no_result_frame)
    
    def rechercher_etudiants():
        filter_text = search_entry.get().strip()
        afficher_etudiants(filter_text)
    
    def clear_search():
        search_entry.delete(0, tk.END)
        afficher_etudiants()
    
    def ajouter_etudiant_ui():
        global student_widgets
        nom = entry_nom.get().strip()
        prenom = entry_prenom.get().strip()
        email = entry_email.get().strip()
        date_naissance = entry_date.get().strip()
        
        if not nom or not prenom or not email or not date_naissance:
            messagebox.showwarning("❌ Erreur de Validation", 
                                 "Tous les champs marqués (*) sont obligatoires")
            return
        
        try:
            ajouter_etudiant(nom, prenom, email, date_naissance)
            messagebox.showinfo("✅ Succès", "Étudiant ajouté avec succès!")
            clear_form()
            afficher_etudiants()
            clear_search()
        except Exception as e:
            messagebox.showerror(u"❌ Erreur", u"Impossible d'ajouter l'étudiant:\n{}".format(e))
    
    def supprimer_etudiant_individuel(etudiant_id):
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
            messagebox.showerror(u"❌ Erreur", u"Impossible de supprimer l'étudiant:\n{}".format(e))
    
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
    
    root.bind('<Control-n>', lambda e: clear_form())
    root.bind('<Control-s>', lambda e: ajouter_etudiant_ui())
    root.bind('<Control-f>', lambda e: search_entry.focus())
    root.bind('<Escape>', lambda e: clear_search())
    
    afficher_etudiants()
    
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (1000 // 2)
    y = (root.winfo_screenheight() // 2) - (750 // 2)
    root.geometry('1000x750+{}+{}'.format(x, y))
    
    entry_nom.focus()
    
    root.mainloop()

if __name__ == "__main__":
    demarrer_interface()