# -*- coding: utf-8 -*-
# gestion_notes_corrige.py

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
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Variables pour stocker les données
        self.etudiants = []
        self.cours = []
        
        self.setup_ui()
        self.charger_donnees()
    
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
        # Titre principal
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x', pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="GESTION DES NOTES", 
                              font=('Arial', 18, 'bold'), 
                              fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        # Notebook pour les onglets
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Onglet 1: Ajouter une note
        self.frame_ajouter = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_ajouter, text="Ajouter Note")
        self.setup_ajouter_note()
        
        # Onglet 2: Consulter les notes
        self.frame_consulter = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_consulter, text="Consulter Notes")
        self.setup_consulter_notes()
        
        # Onglet 3: Moyennes
        self.frame_moyennes = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_moyennes, text="Moyennes")
        self.setup_moyennes()
    
    def setup_ajouter_note(self):
        """Interface pour ajouter une note"""
        # Frame principal
        main_frame = tk.Frame(self.frame_ajouter, bg='white', relief='raised', bd=2)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Titre
        tk.Label(main_frame, text="Ajouter une Note", 
                font=('Arial', 16, 'bold'), bg='white', fg='#2c3e50').pack(pady=10)
        
        # Frame pour les champs
        fields_frame = tk.Frame(main_frame, bg='white')
        fields_frame.pack(pady=20)
        
        # Sélection étudiant
        tk.Label(fields_frame, text="Étudiant:", font=('Arial', 12), bg='white').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.combo_etudiant = ttk.Combobox(fields_frame, width=30, state='readonly')
        self.combo_etudiant.grid(row=0, column=1, padx=5, pady=5)
        
        # Sélection cours
        tk.Label(fields_frame, text="Cours:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.combo_cours = ttk.Combobox(fields_frame, width=30, state='readonly')
        self.combo_cours.grid(row=1, column=1, padx=5, pady=5)
        
        # Année
        tk.Label(fields_frame, text="Année:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.entry_annee = tk.Entry(fields_frame, width=32, font=('Arial', 10))
        self.entry_annee.insert(0, str(datetime.now().year))
        self.entry_annee.grid(row=2, column=1, padx=5, pady=5)
        
        # Note
        tk.Label(fields_frame, text="Note (0-20):", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.entry_note = tk.Entry(fields_frame, width=32, font=('Arial', 10))
        self.entry_note.grid(row=3, column=1, padx=5, pady=5)
        
        # Boutons
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Ajouter Note", command=self.ajouter_note,
                 bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                 width=15, height=2).pack(side='left', padx=10)
        
        tk.Button(btn_frame, text="Effacer", command=self.effacer_champs_ajout,
                 bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                 width=15, height=2).pack(side='left', padx=10)
    
    def setup_consulter_notes(self):
        """Interface pour consulter les notes"""
        # Frame principal
        main_frame = tk.Frame(self.frame_consulter, bg='white', relief='raised', bd=2)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Titre et sélection
        top_frame = tk.Frame(main_frame, bg='white')
        top_frame.pack(fill='x', pady=10)
        
        tk.Label(top_frame, text="Consulter les Notes", 
                font=('Arial', 16, 'bold'), bg='white', fg='#2c3e50').pack()
        
        select_frame = tk.Frame(main_frame, bg='white')
        select_frame.pack(pady=10)
        
        tk.Label(select_frame, text="Sélectionner un étudiant:", 
                font=('Arial', 12), bg='white').pack(side='left', padx=5)
        self.combo_etudiant_consult = ttk.Combobox(select_frame, width=30, state='readonly')
        self.combo_etudiant_consult.pack(side='left', padx=5)
        self.combo_etudiant_consult.bind('<<ComboboxSelected>>', self.afficher_notes_etudiant)
        
        tk.Button(select_frame, text="Actualiser", command=self.actualiser_notes,
                 bg='#3498db', fg='white', font=('Arial', 10)).pack(side='left', padx=10)
        
        # Treeview pour afficher les notes
        tree_frame = tk.Frame(main_frame, bg='white')
        tree_frame.pack(fill='both', expand=True, pady=10)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical')
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal')
        
        self.tree_notes = ttk.Treeview(tree_frame, 
                                      columns=('Cours', 'Enseignant', 'Année', 'Note'),
                                      show='headings',
                                      yscrollcommand=v_scrollbar.set,
                                      xscrollcommand=h_scrollbar.set)
        
        # Configuration des colonnes
        self.tree_notes.heading('Cours', text='Cours')
        self.tree_notes.heading('Enseignant', text='Enseignant')
        self.tree_notes.heading('Année', text='Année')
        self.tree_notes.heading('Note', text='Note')
        
        self.tree_notes.column('Cours', width=200)
        self.tree_notes.column('Enseignant', width=150)
        self.tree_notes.column('Année', width=80)
        self.tree_notes.column('Note', width=80)
        
        # Placement des scrollbars
        v_scrollbar.config(command=self.tree_notes.yview)
        h_scrollbar.config(command=self.tree_notes.xview)
        
        self.tree_notes.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Boutons d'action
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Modifier Note", command=self.modifier_note,
                 bg='#f39c12', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Supprimer Note", command=self.supprimer_note,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
    
    def setup_moyennes(self):
        """Interface pour calculer les moyennes"""
        # Frame principal
        main_frame = tk.Frame(self.frame_moyennes, bg='white', relief='raised', bd=2)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Titre
        tk.Label(main_frame, text="Calcul des Moyennes", 
                font=('Arial', 16, 'bold'), bg='white', fg='#2c3e50').pack(pady=10)
        
        # Sélection étudiant
        select_frame = tk.Frame(main_frame, bg='white')
        select_frame.pack(pady=10)
        
        tk.Label(select_frame, text="Étudiant:", font=('Arial', 12), bg='white').pack(side='left', padx=5)
        self.combo_etudiant_moyenne = ttk.Combobox(select_frame, width=30, state='readonly')
        self.combo_etudiant_moyenne.pack(side='left', padx=5)
        
        tk.Button(select_frame, text="Calculer Moyenne", command=self.calculer_moyenne,
                 bg='#9b59b6', fg='white', font=('Arial', 12, 'bold')).pack(side='left', padx=10)
        
        # Zone d'affichage des résultats
        self.text_moyenne = tk.Text(main_frame, height=15, width=70, 
                                   font=('Arial', 11), bg='#f8f9fa', 
                                   relief='sunken', bd=2)
        self.text_moyenne.pack(pady=20, padx=20, fill='both', expand=True)
    
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
            
            messagebox.showinfo("Succès", "Note ajoutée avec succès!")
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
                
                messagebox.showinfo("Succès", "Note supprimée avec succès!")
                self.afficher_notes_etudiant()
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression: {e}")
    
    def fenetre_modification(self, values):
        """Créer une fenêtre pour modifier une note"""
        fenetre = tk.Toplevel(self.root)
        fenetre.title("Modifier Note")
        fenetre.geometry("400x300")
        fenetre.configure(bg='white')
        fenetre.grab_set()
        
        # Titre
        tk.Label(fenetre, text="Modifier la Note", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        # Champs
        frame_champs = tk.Frame(fenetre, bg='white')
        frame_champs.pack(pady=20)
        
        tk.Label(frame_champs, text="Cours:", bg='white').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        tk.Label(frame_champs, text=values[0], bg='white', relief='sunken', width=30).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_champs, text="Année:", bg='white').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        tk.Label(frame_champs, text=values[2], bg='white', relief='sunken', width=30).grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame_champs, text="Nouvelle Note:", bg='white').grid(row=2, column=0, sticky='w', padx=5, pady=5)
        entry_nouvelle_note = tk.Entry(frame_champs, width=30)
        entry_nouvelle_note.insert(0, values[3])
        entry_nouvelle_note.grid(row=2, column=1, padx=5, pady=5)
        
        # Boutons
        frame_boutons = tk.Frame(fenetre, bg='white')
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
                
                messagebox.showinfo("Succès", "Note modifiée avec succès!")
                fenetre.destroy()
                self.afficher_notes_etudiant()
                
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer une note valide")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la modification: {e}")
        
        tk.Button(frame_boutons, text="Sauvegarder", command=sauvegarder,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=10)
        
        tk.Button(frame_boutons, text="Annuler", command=fenetre.destroy,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=10)
    
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
                self.text_moyenne.insert(tk.END, f"RAPPORT DE NOTES - {etudiant_nom}\n")
                self.text_moyenne.insert(tk.END, "="*50 + "\n\n")
                self.text_moyenne.insert(tk.END, "Aucune note trouvée pour cet étudiant.\n")
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
            
            # Afficher les résultats
            self.text_moyenne.insert(tk.END, f"RAPPORT DE NOTES - {etudiant_nom}\n")
            self.text_moyenne.insert(tk.END, "="*50 + "\n\n")
            
            # Afficher par année
            for annee in sorted(notes_par_annee.keys()):
                self.text_moyenne.insert(tk.END, f"ANNÉE {annee}:\n")
                self.text_moyenne.insert(tk.END, "-" * 20 + "\n")
                
                notes_annee = notes_par_annee[annee]
                somme_annee = sum(note[1] for note in notes_annee)
                moyenne_annee = somme_annee / len(notes_annee)
                
                for cours, note in notes_annee:
                    self.text_moyenne.insert(tk.END, f"  • {cours}: {note:.2f}/20\n")
                
                self.text_moyenne.insert(tk.END, f"\nMoyenne {annee}: {moyenne_annee:.2f}/20\n")
                
                # Appréciation
                if moyenne_annee >= 16:
                    appreciation = "Très Bien"
                elif moyenne_annee >= 14:
                    appreciation = "Bien"
                elif moyenne_annee >= 12:
                    appreciation = "Assez Bien"
                elif moyenne_annee >= 10:
                    appreciation = "Passable"
                else:
                    appreciation = "Insuffisant"
                
                self.text_moyenne.insert(tk.END, f"Appréciation: {appreciation}\n\n")
            
            # Moyenne générale
            if total_notes > 0:
                moyenne_generale = somme_notes / total_notes
                self.text_moyenne.insert(tk.END, "="*50 + "\n")
                self.text_moyenne.insert(tk.END, f"MOYENNE GÉNÉRALE: {moyenne_generale:.2f}/20\n")
                self.text_moyenne.insert(tk.END, f"Nombre total de notes: {total_notes}\n")
                
                # Appréciation générale
                if moyenne_generale >= 16:
                    appreciation_generale = "Excellent parcours"
                elif moyenne_generale >= 14:
                    appreciation_generale = "Bon parcours"
                elif moyenne_generale >= 12:
                    appreciation_generale = "Parcours satisfaisant"
                elif moyenne_generale >= 10:
                    appreciation_generale = "Parcours acceptable"
                else:
                    appreciation_generale = "Parcours à améliorer"
                
                self.text_moyenne.insert(tk.END, f"Appréciation générale: {appreciation_generale}\n")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du calcul de la moyenne: {e}")
    
    def run(self):
        """Lancer l'application"""
        self.root.mainloop()

# Point d'entrée du programme
if __name__ == "__main__":
    print("Démarrage de l'application de gestion des notes...")
    print("Connexion à Cassandra...")
    
    app = GestionNotes()
    
    if app.session:
        print("Connexion réussie!")
        print("Lancement de l'interface graphique...")
        app.run()
    else:
        print("Impossible de démarrer l'application - Problème de connexion à Cassandra")