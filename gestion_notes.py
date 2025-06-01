# -*- coding: utf-8 -*-
# gestion_notes_elegant.py

import tkinter as tk
from tkinter import ttk, messagebox
from cassandra.cluster import Cluster
import uuid
from datetime import datetime

class GestionNotes:
    def __init__(self):
        self.session = self.get_session()
        self.root = tk.Tk()
        self.root.title("Gestion des Notes - Étudiants")
        
        # Taille réduite et centrée
        self.root.geometry("1000x700")
        self.root.configure(bg='#F8F6F0')  # Vanilla ice background
        
        # Centrer la fenêtre sur l'écran
        self.center_window()
        
        # Palette de couleurs élégante
        self.colors = {
            'vanilla_ice': '#F8F6F0',      # Fond principal
            'cosmic': '#2E1065',           # Bleu violet foncé
            'provincial': '#16537e',       # Bleu-vert
            'grape': '#7C3AED',           # Violet
            'light_grape': '#A78BFA',     # Violet clair
            'accent': '#F3F4F6',          # Gris très clair
            'text_dark': '#1F2937',       # Texte foncé
            'text_light': '#6B7280',      # Texte clair
            'success': '#10B981',         # Vert succès
            'warning': '#F59E0B',         # Orange warning
            'danger': '#EF4444'           # Rouge danger
        }
        
        # Variables pour stocker les données
        self.etudiants = []
        self.cours = []
        
        self.setup_styles()
        self.setup_ui()
        self.charger_donnees()
    
    def center_window(self):
        """Centrer la fenêtre sur l'écran"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
    
    def setup_styles(self):
        """Configuration des styles personnalisés"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Style pour les notebooks
        style.configure('Custom.TNotebook', 
                       background=self.colors['vanilla_ice'],
                       borderwidth=0)
        style.configure('Custom.TNotebook.Tab',
                       background=self.colors['accent'],
                       foreground=self.colors['text_dark'],
                       padding=[20, 10],
                       font=('Segoe UI', 11, 'bold'))
        style.map('Custom.TNotebook.Tab',
                 background=[('selected', self.colors['cosmic']),
                           ('active', self.colors['light_grape'])],
                 foreground=[('selected', 'white'),
                           ('active', 'white')])
        
        # Style pour les combobox
        style.configure('Custom.TCombobox',
                       fieldbackground='white',
                       background=self.colors['provincial'],
                       foreground=self.colors['text_dark'],
                       borderwidth=2,
                       relief='flat')
        
        # Style pour les treeview
        style.configure('Custom.Treeview',
                       background='white',
                       foreground=self.colors['text_dark'],
                       fieldbackground='white',
                       borderwidth=0,
                       font=('Segoe UI', 10))
        style.configure('Custom.Treeview.Heading',
                       background=self.colors['cosmic'],
                       foreground='white',
                       font=('Segoe UI', 11, 'bold'),
                       relief='flat')
    
    def create_rounded_button(self, parent, text, command, bg_color, fg_color='white', 
                            width=200, height=45, font_size=12):
        """Créer un bouton arrondi élégant"""
        button_frame = tk.Frame(parent, bg=parent['bg'], highlightthickness=0)
        
        canvas = tk.Canvas(button_frame, width=width, height=height, 
                          highlightthickness=0, relief='flat', bd=0)
        canvas.configure(bg=parent['bg'])
        
        # Créer le rectangle arrondi
        def create_rounded_rect(x1, y1, x2, y2, radius=20):
            points = []
            for x, y in [(x1, y1 + radius), (x1, y1), (x1 + radius, y1),
                        (x2 - radius, y1), (x2, y1), (x2, y1 + radius),
                        (x2, y2 - radius), (x2, y2), (x2 - radius, y2),
                        (x1 + radius, y2), (x1, y2), (x1, y2 - radius)]:
                points.extend([x, y])
            return canvas.create_polygon(points, smooth=True, fill=bg_color, outline='')
        
        rect = create_rounded_rect(2, 2, width-2, height-2, 22)
        
        # Ajouter le texte
        text_item = canvas.create_text(width//2, height//2, text=text, 
                                     fill=fg_color, font=('Segoe UI', font_size, 'bold'))
        
        canvas.pack()
        
        # Effets de survol
        def on_enter(event):
            canvas.itemconfig(rect, fill=self.lighten_color(bg_color))
            canvas.configure(cursor='hand2')
        
        def on_leave(event):
            canvas.itemconfig(rect, fill=bg_color)
            canvas.configure(cursor='')
        
        def on_click(event):
            command()
        
        canvas.bind('<Enter>', on_enter)
        canvas.bind('<Leave>', on_leave)
        canvas.bind('<Button-1>', on_click)
        
        return button_frame
    
    def lighten_color(self, color):
        """Éclaircir une couleur hexadécimale"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        lighter_rgb = tuple(min(255, int(c * 1.2)) for c in rgb)
        return f"#{lighter_rgb[0]:02x}{lighter_rgb[1]:02x}{lighter_rgb[2]:02x}"
    
    def create_elegant_frame(self, parent, title=""):
        """Créer un frame élégant avec ombre"""
        # Frame principal avec ombre
        shadow_frame = tk.Frame(parent, bg='#E5E7EB', relief='flat', bd=0)
        shadow_frame.pack(fill='both', expand=True, padx=25, pady=25)
        
        # Frame de contenu
        content_frame = tk.Frame(shadow_frame, bg='white', relief='flat', bd=0)
        content_frame.pack(fill='both', expand=True, padx=3, pady=3)
        
        if title:
            title_frame = tk.Frame(content_frame, bg=self.colors['cosmic'], height=80)
            title_frame.pack(fill='x', pady=(0, 30))
            title_frame.pack_propagate(False)
            
            title_label = tk.Label(title_frame, text=title,
                                 font=('Segoe UI', 20, 'bold'),
                                 fg='white', bg=self.colors['cosmic'])
            title_label.pack(expand=True)
        
        return content_frame
    
    def get_session(self):
        """Connexion à Cassandra"""
        try:
            cluster = Cluster(['127.0.0.1'])
            session = cluster.connect('gestion_etudiants')
            return session
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de se connecter à Cassandra: {e}")
            return None
    
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        # En-tête principal avec dégradé
        header_frame = tk.Frame(self.root, bg=self.colors['cosmic'], height=80)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Titre principal avec style moderne
        title_label = tk.Label(header_frame, text="🎓 GESTION DES NOTES ÉTUDIANTS",
                              font=('Segoe UI', 22, 'bold'),
                              fg='white', bg=self.colors['cosmic'])
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(header_frame, text="Système de gestion académique moderne",
                                font=('Segoe UI', 11),
                                fg=self.colors['light_grape'], bg=self.colors['cosmic'])
        subtitle_label.pack()
        
        # Container principal
        main_container = tk.Frame(self.root, bg=self.colors['vanilla_ice'])
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Notebook avec style personnalisé
        self.notebook = ttk.Notebook(main_container, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        
        # Onglet 1: Ajouter une note
        self.frame_ajouter = tk.Frame(self.notebook, bg=self.colors['vanilla_ice'])
        self.notebook.add(self.frame_ajouter, text="✏️ Ajouter Note")
        self.setup_ajouter_note()
        
        # Onglet 2: Consulter les notes
        self.frame_consulter = tk.Frame(self.notebook, bg=self.colors['vanilla_ice'])
        self.notebook.add(self.frame_consulter, text="📋 Consulter Notes")
        self.setup_consulter_notes()
        
        # Onglet 3: Moyennes
        self.frame_moyennes = tk.Frame(self.notebook, bg=self.colors['vanilla_ice'])
        self.notebook.add(self.frame_moyennes, text="📊 Moyennes")
        self.setup_moyennes()
    
    def setup_ajouter_note(self):
        """Interface pour ajouter une note"""
        main_frame = self.create_elegant_frame(self.frame_ajouter, "Ajouter une Nouvelle Note")
        
        # Container pour le formulaire
        form_container = tk.Frame(main_frame, bg='white')
        form_container.pack(expand=True, fill='both', padx=30, pady=20)
        
        # Grille pour les champs
        fields_frame = tk.Frame(form_container, bg='white')
        fields_frame.pack(expand=True)
        
        # Style des labels
        label_font = ('Segoe UI', 12, 'bold')
        entry_font = ('Segoe UI', 11)
        
        # Étudiant
        tk.Label(fields_frame, text="👤 Étudiant:", font=label_font, 
                bg='white', fg=self.colors['text_dark']).grid(row=0, column=0, sticky='w', 
                                                             padx=15, pady=15)
        self.combo_etudiant = ttk.Combobox(fields_frame, width=30, state='readonly',
                                          style='Custom.TCombobox', font=entry_font)
        self.combo_etudiant.grid(row=0, column=1, padx=15, pady=15, sticky='ew')
        
        # Cours
        tk.Label(fields_frame, text="📚 Cours:", font=label_font,
                bg='white', fg=self.colors['text_dark']).grid(row=1, column=0, sticky='w',
                                                             padx=15, pady=15)
        self.combo_cours = ttk.Combobox(fields_frame, width=30, state='readonly',
                                       style='Custom.TCombobox', font=entry_font)
        self.combo_cours.grid(row=1, column=1, padx=15, pady=15, sticky='ew')
        
        # Année
        tk.Label(fields_frame, text="📅 Année:", font=label_font,
                bg='white', fg=self.colors['text_dark']).grid(row=2, column=0, sticky='w',
                                                             padx=15, pady=15)
        self.entry_annee = tk.Entry(fields_frame, width=32, font=entry_font,
                                   relief='flat', bd=5, bg=self.colors['accent'])
        self.entry_annee.insert(0, str(datetime.now().year))
        self.entry_annee.grid(row=2, column=1, padx=15, pady=15, sticky='ew')
        
        # Note
        tk.Label(fields_frame, text="🎯 Note (0-20):", font=label_font,
                bg='white', fg=self.colors['text_dark']).grid(row=3, column=0, sticky='w',
                                                             padx=15, pady=15)
        self.entry_note = tk.Entry(fields_frame, width=32, font=entry_font,
                                  relief='flat', bd=5, bg=self.colors['accent'])
        self.entry_note.grid(row=3, column=1, padx=15, pady=15, sticky='ew')
        
        # Configuration de la grille
        fields_frame.grid_columnconfigure(1, weight=1)
        
        # Boutons avec style moderne - CORRIGÉ
        btn_container = tk.Frame(form_container, bg='white')
        btn_container.pack(pady=20, fill='x')
        
        btn_frame = tk.Frame(btn_container, bg='white')
        btn_frame.pack(expand=True)
        
        # Bouton Ajouter
        btn_ajouter = self.create_rounded_button(btn_frame, "✅ Ajouter Note", 
                                                self.ajouter_note, self.colors['success'],
                                                width=180, height=45, font_size=12)
        btn_ajouter.pack(side='left', padx=10)
        
        # Bouton Effacer
        btn_effacer = self.create_rounded_button(btn_frame, "🗑️ Effacer", 
                                               self.effacer_champs_ajout, self.colors['warning'],
                                               width=180, height=45, font_size=12)
        btn_effacer.pack(side='left', padx=10)
    
    def setup_consulter_notes(self):
        """Interface pour consulter les notes"""
        main_frame = self.create_elegant_frame(self.frame_consulter, "Consulter les Notes")
        
        # Section de sélection
        select_container = tk.Frame(main_frame, bg='white')
        select_container.pack(fill='x', padx=30, pady=15)
        
        select_frame = tk.Frame(select_container, bg=self.colors['accent'], relief='flat', bd=0)
        select_frame.pack(fill='x', pady=5)
        
        tk.Label(select_frame, text="👤 Sélectionner un étudiant:",
                font=('Segoe UI', 12, 'bold'), bg=self.colors['accent'],
                fg=self.colors['text_dark']).pack(side='left', padx=15, pady=10)
        
        self.combo_etudiant_consult = ttk.Combobox(select_frame, width=30, state='readonly',
                                                  style='Custom.TCombobox',
                                                  font=('Segoe UI', 11))
        self.combo_etudiant_consult.pack(side='left', padx=15, pady=10)
        self.combo_etudiant_consult.bind('<<ComboboxSelected>>', self.afficher_notes_etudiant)
        
        # Bouton actualiser moderne
        btn_actualiser = self.create_rounded_button(select_frame, "🔄 Actualiser",
                                                   self.actualiser_notes, self.colors['provincial'],
                                                   width=130, height=35, font_size=11)
        btn_actualiser.pack(side='left', padx=15, pady=10)
        
        # Container pour le tableau
        table_container = tk.Frame(main_frame, bg='white')
        table_container.pack(fill='both', expand=True, padx=30, pady=15)
        
        # Treeview avec style personnalisé
        tree_frame = tk.Frame(table_container, bg='white', relief='flat', bd=2)
        tree_frame.pack(fill='both', expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical')
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal')
        
        self.tree_notes = ttk.Treeview(tree_frame,
                                      columns=('Cours', 'Enseignant', 'Année', 'Note'),
                                      show='headings',
                                      style='Custom.Treeview',
                                      yscrollcommand=v_scrollbar.set,
                                      xscrollcommand=h_scrollbar.set)
        
        # Configuration des colonnes
        self.tree_notes.heading('Cours', text='📚 Cours')
        self.tree_notes.heading('Enseignant', text='👨‍🏫 Enseignant')
        self.tree_notes.heading('Année', text='📅 Année')
        self.tree_notes.heading('Note', text='🎯 Note')
        
        self.tree_notes.column('Cours', width=220)
        self.tree_notes.column('Enseignant', width=180)
        self.tree_notes.column('Année', width=80)
        self.tree_notes.column('Note', width=80)
        
        # Placement
        v_scrollbar.config(command=self.tree_notes.yview)
        h_scrollbar.config(command=self.tree_notes.xview)
        
        self.tree_notes.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Boutons d'action
        action_container = tk.Frame(main_frame, bg='white')
        action_container.pack(pady=20)
        
        action_frame = tk.Frame(action_container, bg='white')
        action_frame.pack()
        
        btn_modifier = self.create_rounded_button(action_frame, "✏️ Modifier Note",
                                                 self.modifier_note, self.colors['grape'],
                                                 width=160, height=40, font_size=11)
        btn_modifier.pack(side='left', padx=10)
        
        btn_supprimer = self.create_rounded_button(action_frame, "🗑️ Supprimer Note",
                                                  self.supprimer_note, self.colors['danger'],
                                                  width=160, height=40, font_size=11)
        btn_supprimer.pack(side='left', padx=10)
    
    def setup_moyennes(self):
        """Interface pour calculer les moyennes"""
        main_frame = self.create_elegant_frame(self.frame_moyennes, "Calcul des Moyennes")
        
        # Section de sélection
        select_container = tk.Frame(main_frame, bg='white')
        select_container.pack(fill='x', padx=30, pady=15)
        
        select_frame = tk.Frame(select_container, bg=self.colors['accent'], relief='flat', bd=0)
        select_frame.pack(fill='x', pady=5)
        
        tk.Label(select_frame, text="👤 Étudiant:",
                font=('Segoe UI', 12, 'bold'), bg=self.colors['accent'],
                fg=self.colors['text_dark']).pack(side='left', padx=15, pady=10)
        
        self.combo_etudiant_moyenne = ttk.Combobox(select_frame, width=30, state='readonly',
                                                  style='Custom.TCombobox',
                                                  font=('Segoe UI', 11))
        self.combo_etudiant_moyenne.pack(side='left', padx=15, pady=10)
        
        btn_calculer = self.create_rounded_button(select_frame, "📊 Calculer Moyenne",
                                                 self.calculer_moyenne, self.colors['grape'],
                                                 width=180, height=35, font_size=11)
        btn_calculer.pack(side='left', padx=15, pady=10)
        
        # Zone d'affichage des résultats
        result_container = tk.Frame(main_frame, bg='white')
        result_container.pack(fill='both', expand=True, padx=30, pady=15)
        
        # Frame avec bordure élégante pour le texte
        text_frame = tk.Frame(result_container, bg=self.colors['accent'], relief='flat', bd=2)
        text_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.text_moyenne = tk.Text(text_frame, font=('Consolas', 11),
                                   bg='white', fg=self.colors['text_dark'],
                                   relief='flat', bd=5, wrap='word')
        self.text_moyenne.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Scrollbar pour le texte
        text_scroll = ttk.Scrollbar(text_frame, orient='vertical', command=self.text_moyenne.yview)
        self.text_moyenne.configure(yscrollcommand=text_scroll.set)
        text_scroll.pack(side='right', fill='y')
    
    def charger_donnees(self):
        """Charger les étudiants et cours depuis Cassandra"""
        if not self.session:
            return
            
        try:
            # Charger les étudiants
            rows = self.session.execute("SELECT id, nom, prenom FROM etudiants")
            self.etudiants = [(str(row.id), f"{row.nom} {row.prenom}") for row in rows]
            
            # Charger les cours
            rows = self.session.execute("SELECT id, nom, enseignant FROM cours")
            self.cours = [(str(row.id), f"{row.nom} ({row.enseignant})") for row in rows]
            
            # Mettre à jour les combobox
            self.mettre_a_jour_combobox()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des données: {e}")
    
    def mettre_a_jour_combobox(self):
        """Mettre à jour toutes les combobox"""
        etudiant_values = [etudiant[1] for etudiant in self.etudiants]
        cours_values = [cours[1] for cours in self.cours]
        
        self.combo_etudiant['values'] = etudiant_values
        self.combo_etudiant_consult['values'] = etudiant_values
        self.combo_etudiant_moyenne['values'] = etudiant_values
        self.combo_cours['values'] = cours_values
    
    def ajouter_note(self):
        """Ajouter une nouvelle note"""
        try:
            # Validation des champs
            if not self.combo_etudiant.get() or not self.combo_cours.get():
                messagebox.showerror("Erreur", "Veuillez sélectionner un étudiant et un cours")
                return
            
            if not self.entry_annee.get().strip() or not self.entry_note.get().strip():
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
                return
            
            # Conversion et validation des valeurs numériques
            try:
                annee = int(self.entry_annee.get().strip())
                note = float(self.entry_note.get().strip())
            except ValueError:
                messagebox.showerror("Erreur", "L'année doit être un nombre entier et la note un nombre décimal")
                return
            
            if not (0 <= note <= 20):
                messagebox.showerror("Erreur", "La note doit être entre 0 et 20")
                return
            
            if annee < 1900 or annee > 2100:
                messagebox.showerror("Erreur", "L'année doit être valide")
                return
            
            # Récupérer les IDs
            etudiant_nom = self.combo_etudiant.get()
            cours_nom = self.combo_cours.get()
            
            etudiant_id = None
            cours_id = None
            
            # Trouver l'ID de l'étudiant
            for etudiant in self.etudiants:
                if etudiant[1] == etudiant_nom:
                    etudiant_id = etudiant[0]
                    break
            
            # Trouver l'ID du cours
            for cours in self.cours:
                if cours[1] == cours_nom:
                    cours_id = cours[0]
                    break
            
            if not etudiant_id or not cours_id:
                messagebox.showerror("Erreur", "Étudiant ou cours non trouvé")
                return
            
            # Vérifier si une note existe déjà pour cette combinaison
            check_query = """
            SELECT note FROM notes 
            WHERE etudiant_id = %s AND cours_id = %s AND annee = %s
            """
            existing = list(self.session.execute(check_query, (
                uuid.UUID(etudiant_id), 
                uuid.UUID(cours_id), 
                annee
            )))
            
            if existing:
                response = messagebox.askyesno(
                    "Note existante", 
                    f"Une note existe déjà pour cet étudiant dans ce cours pour l'année {annee}.\n"
                    f"Note actuelle: {existing[0].note}\n"
                    f"Voulez-vous la remplacer par {note}?"
                )
                if not response:
                    return
            
            # Insérer ou mettre à jour dans Cassandra
            insert_query = """
            INSERT INTO notes (etudiant_id, cours_id, annee, note) 
            VALUES (%s, %s, %s, %s)
            """
            
            self.session.execute(insert_query, (
                uuid.UUID(etudiant_id),
                uuid.UUID(cours_id),
                annee,
                note
            ))
            
            messagebox.showinfo("Succès", "✅ Note ajoutée avec succès!")
            self.effacer_champs_ajout()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {str(e)}")
            print(f"Erreur détaillée: {e}")
    
    def effacer_champs_ajout(self):
        """Effacer les champs du formulaire d'ajout"""
        self.combo_etudiant.set('')
        self.combo_cours.set('')
        self.entry_annee.delete(0, tk.END)
        self.entry_annee.insert(0, str(datetime.now().year))
        self.entry_note.delete(0, tk.END)
    
    def afficher_notes_etudiant(self, event=None):
        """Afficher les notes d'un étudiant sélectionné"""
        if not self.combo_etudiant_consult.get():
            return
        
        try:
            # Vider le treeview
            for item in self.tree_notes.get_children():
                self.tree_notes.delete(item)
            
            # Récupérer l'ID de l'étudiant
            etudiant_nom = self.combo_etudiant_consult.get()
            etudiant_id = None
            
            for etudiant in self.etudiants:
                if etudiant[1] == etudiant_nom:
                    etudiant_id = etudiant[0]
                    break
            
            if not etudiant_id:
                return
            
            # Requête simplifiée pour récupérer les notes avec ALLOW FILTERING
            query = "SELECT cours_id, annee, note FROM notes WHERE etudiant_id = %s ALLOW FILTERING"
            rows = self.session.execute(query, (uuid.UUID(etudiant_id),))
            
            # Pour chaque note, récupérer les infos du cours
            for row in rows:
                # Récupérer les infos du cours
                cours_query = "SELECT nom, enseignant FROM cours WHERE id = %s"
                cours_info = list(self.session.execute(cours_query, (row.cours_id,)))
                
                if cours_info:
                    cours_nom = cours_info[0].nom
                    enseignant = cours_info[0].enseignant
                    
                    self.tree_notes.insert('', 'end', values=(
                        cours_nom,
                        enseignant,
                        row.annee,
                        f"{row.note:.2f}"
                    ))
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage des notes: {e}")
    
    def actualiser_notes(self):
        """Actualiser l'affichage des notes"""
        self.charger_donnees()
        self.afficher_notes_etudiant()
    
    def modifier_note(self):
        """Modifier une note sélectionnée"""
        selection = self.tree_notes.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner une note à modifier")
            return
        
        # Récupérer les valeurs de la ligne sélectionnée
        item = self.tree_notes.item(selection[0])
        values = item['values']
        
        # Créer une fenêtre de modification
        self.fenetre_modification(values)
    
    def supprimer_note(self):
        """Supprimer une note sélectionnée"""
        selection = self.tree_notes.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner une note à supprimer")
            return
        
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cette note?"):
            try:
                item = self.tree_notes.item(selection[0])
                values = item['values']
                
                # Récupérer les IDs
                etudiant_nom = self.combo_etudiant_consult.get()
                etudiant_id = None
                for etudiant in self.etudiants:
                    if etudiant[1] == etudiant_nom:
                        etudiant_id = etudiant[0]
                        break
                
                cours_nom = values[0]
                cours_id = None
                for cours in self.cours:
                    if cours[1].startswith(cours_nom):
                        cours_id = cours[0]
                        break
                
                annee = int(values[2])
                
                # Supprimer de Cassandra
                query = "DELETE FROM notes WHERE etudiant_id = %s AND cours_id = %s AND annee = %s"
                self.session.execute(query, (uuid.UUID(etudiant_id), uuid.UUID(cours_id), annee))
                
                messagebox.showinfo("Succès", "✅ Note supprimée avec succès!")
                self.afficher_notes_etudiant()
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression: {e}")
    
    def fenetre_modification(self, values):
        """Créer une fenêtre pour modifier une note"""
        fenetre = tk.Toplevel(self.root)
        fenetre.title("Modifier Note")
        fenetre.geometry("450x350")
        fenetre.configure(bg=self.colors['vanilla_ice'])
        fenetre.grab_set()
        
        # Centrer la fenêtre
        fenetre.update_idletasks()
        width = fenetre.winfo_width()
        height = fenetre.winfo_height()
        x = (fenetre.winfo_screenwidth() // 2) - (width // 2)
        y = (fenetre.winfo_screenheight() // 2) - (height // 2)
        fenetre.geometry(f'+{x}+{y}')
        
        # En-tête
        header_frame = tk.Frame(fenetre, bg=self.colors['cosmic'], height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="✏️ Modifier la Note",
                font=('Segoe UI', 16, 'bold'), bg=self.colors['cosmic'], fg='white').pack(expand=True)
        
        # Contenu principal
        main_frame = tk.Frame(fenetre, bg='white', relief='flat', bd=0)
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Champs
        frame_champs = tk.Frame(main_frame, bg='white')
        frame_champs.pack(expand=True, pady=20)
        
        label_font = ('Segoe UI', 11, 'bold')
        
        tk.Label(frame_champs, text="📚 Cours:", bg='white', font=label_font,
                fg=self.colors['text_dark']).grid(row=0, column=0, sticky='w', padx=10, pady=10)
        tk.Label(frame_champs, text=values[0], bg=self.colors['accent'], relief='flat',
                width=30, font=('Segoe UI', 10), anchor='w').grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(frame_champs, text="📅 Année:", bg='white', font=label_font,
                fg=self.colors['text_dark']).grid(row=1, column=0, sticky='w', padx=10, pady=10)
        tk.Label(frame_champs, text=values[2], bg=self.colors['accent'], relief='flat',
                width=30, font=('Segoe UI', 10), anchor='w').grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(frame_champs, text="🎯 Nouvelle Note:", bg='white', font=label_font,
                fg=self.colors['text_dark']).grid(row=2, column=0, sticky='w', padx=10, pady=10)
        entry_nouvelle_note = tk.Entry(frame_champs, width=32, font=('Segoe UI', 10),
                                      relief='flat', bd=5, bg=self.colors['accent'])
        entry_nouvelle_note.insert(0, values[3])
        entry_nouvelle_note.grid(row=2, column=1, padx=10, pady=10)
        
        # Boutons
        frame_boutons = tk.Frame(main_frame, bg='white')
        frame_boutons.pack(pady=20)
        
        def sauvegarder():
            try:
                nouvelle_note = float(entry_nouvelle_note.get())
                if not (0 <= nouvelle_note <= 20):
                    messagebox.showerror("Erreur", "La note doit être entre 0 et 20")
                    return
                
                # Récupérer les IDs
                etudiant_nom = self.combo_etudiant_consult.get()
                etudiant_id = None
                for etudiant in self.etudiants:
                    if etudiant[1] == etudiant_nom:
                        etudiant_id = etudiant[0]
                        break
                
                cours_nom = values[0]
                cours_id = None
                for cours in self.cours:
                    if cours[1].startswith(cours_nom):
                        cours_id = cours[0]
                        break
                
                annee = int(values[2])
                
                # Mettre à jour dans Cassandra
                query = """
                UPDATE notes SET note = %s 
                WHERE etudiant_id = %s AND cours_id = %s AND annee = %s
                """
                self.session.execute(query, (nouvelle_note, uuid.UUID(etudiant_id), uuid.UUID(cours_id), annee))
                
                messagebox.showinfo("Succès", "✅ Note modifiée avec succès!")
                fenetre.destroy()
                self.afficher_notes_etudiant()
                
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer une note valide")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la modification: {e}")
        
        btn_sauvegarder = self.create_rounded_button(frame_boutons, "💾 Sauvegarder",
                                                    sauvegarder, self.colors['success'],
                                                    width=140, height=35, font_size=11)
        btn_sauvegarder.pack(side='left', padx=10)
        
        btn_annuler = self.create_rounded_button(frame_boutons, "❌ Annuler",
                                               fenetre.destroy, self.colors['danger'],
                                               width=140, height=35, font_size=11)
        btn_annuler.pack(side='left', padx=10)
    
    def calculer_moyenne(self):
        """Calculer et afficher la moyenne d'un étudiant"""
        if not self.combo_etudiant_moyenne.get():
            messagebox.showwarning("Attention", "Veuillez sélectionner un étudiant")
            return
        
        try:
            # Vider la zone de texte
            self.text_moyenne.delete(1.0, tk.END)
            
            # Récupérer l'ID de l'étudiant
            etudiant_nom = self.combo_etudiant_moyenne.get()
            etudiant_id = None
            
            for etudiant in self.etudiants:
                if etudiant[1] == etudiant_nom:
                    etudiant_id = etudiant[0]
                    break
            
            if not etudiant_id:
                return
            
            # Requête pour récupérer toutes les notes de l'étudiant avec ALLOW FILTERING
            query = "SELECT note, annee, cours_id FROM notes WHERE etudiant_id = %s ALLOW FILTERING"
            rows = list(self.session.execute(query, (uuid.UUID(etudiant_id),)))
            
            if not rows:
                self.text_moyenne.insert(tk.END, f"📊 RAPPORT DE NOTES - {etudiant_nom}\n")
                self.text_moyenne.insert(tk.END, "="*60 + "\n\n")
                self.text_moyenne.insert(tk.END, "❌ Aucune note trouvée pour cet étudiant.\n")
                return
            
            notes_par_annee = {}
            total_notes = 0
            somme_notes = 0
            
            # Organiser les notes par année et récupérer les noms des cours
            for row in rows:
                # Récupérer le nom du cours
                cours_query = "SELECT nom FROM cours WHERE id = %s"
                cours_info = list(self.session.execute(cours_query, (row.cours_id,)))
                cours_nom = cours_info[0].nom if cours_info else "Cours inconnu"
                
                annee = row.annee
                if annee not in notes_par_annee:
                    notes_par_annee[annee] = []
                notes_par_annee[annee].append((cours_nom, row.note))
                total_notes += 1
                somme_notes += row.note
            
            # Afficher les résultats avec style
            self.text_moyenne.insert(tk.END, f"📊 RAPPORT DE NOTES - {etudiant_nom}\n")
            self.text_moyenne.insert(tk.END, "="*60 + "\n\n")
            
            # Afficher par année
            for annee in sorted(notes_par_annee.keys()):
                self.text_moyenne.insert(tk.END, f"📅 ANNÉE {annee}:\n")
                self.text_moyenne.insert(tk.END, "-" * 30 + "\n")
                
                notes_annee = notes_par_annee[annee]
                somme_annee = sum(note[1] for note in notes_annee)
                moyenne_annee = somme_annee / len(notes_annee)
                
                for cours, note in notes_annee:
                    self.text_moyenne.insert(tk.END, f"  📚 {cours}: {note:.2f}/20\n")
                
                self.text_moyenne.insert(tk.END, f"\n🎯 Moyenne {annee}: {moyenne_annee:.2f}/20\n")
                
                # Appréciation avec emojis
                if moyenne_annee >= 16:
                    appreciation = "🏆 Très Bien"
                elif moyenne_annee >= 14:
                    appreciation = "🥈 Bien"
                elif moyenne_annee >= 12:
                    appreciation = "🥉 Assez Bien"
                elif moyenne_annee >= 10:
                    appreciation = "✅ Passable"
                else:
                    appreciation = "❌ Insuffisant"
                
                self.text_moyenne.insert(tk.END, f"📝 Appréciation: {appreciation}\n\n")
            
            # Moyenne générale
            if total_notes > 0:
                moyenne_generale = somme_notes / total_notes
                self.text_moyenne.insert(tk.END, "="*60 + "\n")
                self.text_moyenne.insert(tk.END, f"🎯 MOYENNE GÉNÉRALE: {moyenne_generale:.2f}/20\n")
                self.text_moyenne.insert(tk.END, f"📊 Nombre total de notes: {total_notes}\n")
                
                # Appréciation générale
                if moyenne_generale >= 16:
                    appreciation_generale = "🌟 Excellent parcours"
                elif moyenne_generale >= 14:
                    appreciation_generale = "⭐ Bon parcours"
                elif moyenne_generale >= 12:
                    appreciation_generale = "👍 Parcours satisfaisant"
                elif moyenne_generale >= 10:
                    appreciation_generale = "✔️ Parcours acceptable"
                else:
                    appreciation_generale = "⚠️ Parcours à améliorer"
                
                self.text_moyenne.insert(tk.END, f"🏅 Appréciation générale: {appreciation_generale}\n")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du calcul de la moyenne: {e}")
    
    def run(self):
        """Lancer l'application"""
        # Centrer la fenêtre après le chargement complet
        self.root.update_idletasks()
        self.center_window()
        self.root.mainloop()

# Point d'entrée du programme
if __name__ == "__main__":
    print("🚀 Démarrage de l'application de gestion des notes...")
    print("🔌 Connexion à Cassandra...")
    
    app = GestionNotes()
    
    if app.session:
        print("✅ Connexion réussie!")
        print("🎨 Lancement de l'interface graphique élégante...")
        app.run()
    else:
        print("❌ Impossible de démarrer l'application - Problème de connexion à Cassandra")