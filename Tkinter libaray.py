
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

class Livre:
    def __init__(self, titre, auteur, genre):
        self.titre = titre
        self.auteur = auteur
        self.genre = genre
        self.statut = "Disponible"
        self.date_emprunt = None
        self.date_retour_prevue = None
        self.emprunteur = None

    def emprunter(self, emprunteur):
        self.statut = "Emprunté"
        self.date_emprunt = datetime.now()
        self.date_retour_prevue = self.date_emprunt + timedelta(days=14)
        self.emprunteur = emprunteur

    def retourner(self):
        self.statut = "Disponible"
        self.date_emprunt = None
        self.date_retour_prevue = None
        self.emprunteur = None

    def est_en_retard(self):
        if self.statut == "Emprunté":
            return datetime.now() > self.date_retour_prevue
        return False


class BibliothequeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion de Bibliothèque")
        self.geometry("480x700")
        self.configure(bg="#EAEAEA")

        self.livres = []
        self.creer_interface()
        self.charger_donnees_test()

    def charger_donnees_test(self):
        livres_test = [
            ("Python pour débutants", "A. Dupont", "Informatique"),
            ("Le Petit Prince", "Saint-Exupéry", "Littérature"),
            ("Clean Code", "Robert Martin", "Programmation")
        ]
        for livre in livres_test:
            self.livres.append(Livre(*livre))

    def creer_interface(self):
        # Cadre principal
        main_frame = tk.Frame(self, bg="#ffffff", padx=20, pady=20, bd=5, relief="solid")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Titres
        title_label = tk.Label(main_frame, text="Bibliothèque", font=("Arial", 24, "bold"), fg="#3D85C6", bg="#ffffff")
        title_label.pack(pady=(0, 20))

        # Description
        description = tk.Label(main_frame, text="Gérez les livres, emprunts et retours.", font=("Arial", 14), bg="#ffffff")
        description.pack(pady=(0, 20))

        # Boutons principaux
        boutons = [
            ("Ajouter Livre", self.ajouter_livre),
            ("Supprimer Livre", self.supprimer_livre),
            ("Emprunter Livre", self.emprunter_livre),
            ("Retourner Livre", self.retourner_livre),
            ("Afficher Livres", self.afficher_livres),
            ("Rechercher Livre", self.rechercher_livre)
        ]

        for texte, commande in boutons:
            btn = tk.Button(main_frame, text=texte, command=commande, 
                            bg="#3D85C6", fg="white", font=("Arial", 12), 
                            relief="flat", bd=3, width=25, height=2)
            btn.pack(pady=15, fill=tk.X)
            # Séparateur
            tk.Frame(main_frame, height=1, bg="#EAEAEA").pack(fill=tk.X)

    def ajouter_livre(self):
        fenetre = tk.Toplevel(self)
        fenetre.title("Ajouter un livre")
        fenetre.geometry("400x300")
        fenetre.configure(bg="#F7F7F7")

        # Labels et champs de texte
        tk.Label(fenetre, text="Titre:", font=("Arial", 12), bg="#F7F7F7").pack(pady=10)
        titre_entry = tk.Entry(fenetre, font=("Arial", 12), width=30)
        titre_entry.pack(pady=5)
        
        tk.Label(fenetre, text="Auteur:", font=("Arial", 12), bg="#F7F7F7").pack(pady=10)
        auteur_entry = tk.Entry(fenetre, font=("Arial", 12), width=30)
        auteur_entry.pack(pady=5)
        
        tk.Label(fenetre, text="Genre:", font=("Arial", 12), bg="#F7F7F7").pack(pady=10)
        genre_entry = tk.Entry(fenetre, font=("Arial", 12), width=30)
        genre_entry.pack(pady=5)
        
        def valider():
            titre = titre_entry.get()
            auteur = auteur_entry.get()
            genre = genre_entry.get()

            if not all([titre, auteur, genre]):
                messagebox.showerror("Erreur", "Tous les champs sont requis")
                return
            
            for livre in self.livres:
                if livre.titre.lower() == titre.lower():
                    messagebox.showerror("Erreur", "Ce livre existe déjà")
                    return
            
            self.livres.append(Livre(titre, auteur, genre))
            messagebox.showinfo("Succès", "Livre ajouté avec succès")
            fenetre.destroy()
        
        tk.Button(fenetre, text="Ajouter", command=valider, font=("Arial", 14), bg="#3D85C6", fg="white").pack(pady=20)

    def supprimer_livre(self):
        fenetre = tk.Toplevel(self)
        fenetre.title("Supprimer un livre")
        fenetre.geometry("400x250")
        fenetre.configure(bg="#F7F7F7")
        
        tk.Label(fenetre, text="Titre du livre à supprimer:", font=("Arial", 12), bg="#F7F7F7").pack(pady=10)
        titre_entry = tk.Entry(fenetre, font=("Arial", 12), width=30)
        titre_entry.pack(pady=5)
        
        def valider():
            titre = titre_entry.get()
            if not titre:
                messagebox.showerror("Erreur", "Veuillez entrer un titre")
                return
                
            for livre in self.livres:
                if livre.titre.lower() == titre.lower():
                    if livre.statut != "Disponible":
                        messagebox.showerror("Erreur", "Ce livre est actuellement emprunté")
                        return
                    self.livres.remove(livre)
                    messagebox.showinfo("Succès", "Livre supprimé avec succès")
                    fenetre.destroy()
                    return
            
            messagebox.showerror("Erreur", "Livre non trouvé")
        
        tk.Button(fenetre, text="Supprimer", command=valider, font=("Arial", 14), bg="#D32F2F", fg="white").pack(pady=20)

    def emprunter_livre(self):
        fenetre = tk.Toplevel(self)
        fenetre.title("Emprunter un livre")
        fenetre.geometry("400x300")
        fenetre.configure(bg="#F7F7F7")
        
        tk.Label(fenetre, text="Titre du livre à emprunter:", font=("Arial", 12), bg="#F7F7F7").pack(pady=10)
        titre_entry = tk.Entry(fenetre, font=("Arial", 12), width=30)
        titre_entry.pack(pady=5)
        
        tk.Label(fenetre, text="Nom emprunteur:", font=("Arial", 12), bg="#F7F7F7").pack(pady=10)
        emprunteur_entry = tk.Entry(fenetre, font=("Arial", 12), width=30)
        emprunteur_entry.pack(pady=5)
        
        def valider():
            titre = titre_entry.get()
            emprunteur = emprunteur_entry.get()

            if not all([titre, emprunteur]):
                messagebox.showerror("Erreur", "Tous les champs sont requis")
                return
            
            for livre in self.livres:
                if livre.titre.lower() == titre.lower():
                    if livre.statut != "Disponible":
                        messagebox.showerror("Erreur", "Ce livre est déjà emprunté")
                        return
                    livre.emprunter(emprunteur)
                    messagebox.showinfo("Succès", f"Livre emprunté par {emprunteur}")
                    fenetre.destroy()
                    return
            
            messagebox.showerror("Erreur", "Livre non trouvé")
        
        tk.Button(fenetre, text="Emprunter", command=valider, font=("Arial", 14), bg="#3D85C6", fg="white").pack(pady=20)

    def retourner_livre(self):
        fenetre = tk.Toplevel(self)
        fenetre.title("Retourner un livre")
        fenetre.geometry("400x250")
        fenetre.configure(bg="#F7F7F7")
        
        tk.Label(fenetre, text="Titre du livre à retourner:", font=("Arial", 12), bg="#F7F7F7").pack(pady=10)
        titre_entry = tk.Entry(fenetre, font=("Arial", 12), width=30)
        titre_entry.pack(pady=5)
        
        def valider():
            titre = titre_entry.get()
            if not titre:
                messagebox.showerror("Erreur", "Veuillez entrer un titre")
                return
                
            for livre in self.livres:
                if livre.titre.lower() == titre.lower():
                    if livre.statut != "Emprunté":
                        messagebox.showerror("Erreur", "Ce livre n'est pas emprunté")
                        return
                    livre.retourner()
                    message = f"Livre retourné"
                    if livre.est_en_retard():
                        message += " (en retard!)"
                    messagebox.showinfo("Succès", message)
                    fenetre.destroy()
                    return
            
            messagebox.showerror("Erreur", "Livre non trouvé")
        
        tk.Button(fenetre, text="Retourner", command=valider, font=("Arial", 14), bg="#3D85C6", fg="white").pack(pady=20)

    def afficher_livres(self):
        fenetre = tk.Toplevel(self)
        fenetre.title("Liste des livres")
        fenetre.geometry("500x400")
        fenetre.configure(bg="#F7F7F7")
        
        cadre = tk.Frame(fenetre)
        cadre.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(cadre)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        texte = tk.Text(cadre, wrap=tk.WORD, yscrollcommand=scrollbar.set, font=("Arial", 12))
        texte.pack(fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=texte.yview)
        
        if not self.livres:
            texte.insert(tk.END, "Aucun livre dans la bibliothèque")
        else:
            for livre in self.livres:
                texte.insert(tk.END, f"Titre: {livre.titre}\n")
                texte.insert(tk.END, f"Auteur: {livre.auteur}\n")
                texte.insert(tk.END, f"Genre: {livre.genre}\n")
                texte.insert(tk.END, f"Statut: {livre.statut}")
                
                if livre.statut == "Emprunté":
                    texte.insert(tk.END, f" (par {livre.emprunteur})\n")
                    texte.insert(tk.END, f"Retour prévu: {livre.date_retour_prevue.strftime('%d/%m/%Y')}")
                    if livre.est_en_retard():
                        texte.insert(tk.END, " - EN RETARD!")
                texte.insert(tk.END, "\n\n")
        
        texte.config(state=tk.DISABLED)

    def rechercher_livre(self):
        fenetre = tk.Toplevel(self)
        fenetre.title("Rechercher un livre")
        
        tk.Label(fenetre, text="Titre du livre:", font=("Arial", 12), bg="#F7F7F7").grid(row=0, column=0, padx=5, pady=5)
        titre_entry = tk.Entry(fenetre, font=("Arial", 12), width=30)
        titre_entry.grid(row=0, column=1, padx=5, pady=5)
        
        def valider():
            titre = titre_entry.get()
            if not titre:
                messagebox.showerror("Erreur", "Veuillez entrer un titre")
                return
                
            for livre in self.livres:
                if livre.titre.lower() == titre.lower():
                    details = [
                        f"Titre: {livre.titre}",
                        f"Auteur: {livre.auteur}",
                        f"Genre: {livre.genre}",
                        f"Statut: {livre.statut}"
                    ]
                    if livre.statut == "Emprunté":
                        details.append(f"Emprunteur: {livre.emprunteur}")
                        details.append(f"Date retour: {livre.date_retour_prevue.strftime('%d/%m/%Y')}")
                        if livre.est_en_retard():
                            details.append("⚠ EN RETARD!")
                    messagebox.showinfo("Détails", "\n".join(details))
                    return
            
            messagebox.showerror("Erreur", "Livre non trouvé")
        
        tk.Button(fenetre, text="Rechercher", command=valider, font=("Arial", 14), bg="#3D85C6", fg="white").grid(row=1, columnspan=2, pady=10)


if __name__ == "__main__":
    app = BibliothequeApp()
    app.mainloop()