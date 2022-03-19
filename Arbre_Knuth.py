# -*- coding: utf-8 -*-

__author__ = "Gabriel Dosne"

# Commandes recommandées :
#   creer_arbre_knuth()

class Noeud:
    def __init__(self, valeur=None) -> None:
        self.valeur = valeur
        self.enfants = []

    def est_feuille(self) -> bool:
        """
        Renvoie un booléen, qui est vrai si l'instance courante est une feuille
        et fausse si l'instance courante a des enfants.
        """
        return self.enfants == []

    def ajouter(self, valeur=None) -> None:
        """
        Ajoute un noeud de valeur 'valeur' à l'instance courante.
        Ne renvoie rien.
        """
        if isinstance(valeur, Noeud):
            self.enfants.append(valeur)
        else:
            self.enfants.append(Noeud(valeur))

    def liste_enfants_recursif2(self) -> str:
        """
        Fonction qui génére du code Graphviz (incomplet) qui représente
        l'arbre de l'instance courante.
        Fonction utilisée par la fonction 'graphviz_export'.
        Renvoie une chaîne de caractères.
        """
        valeur_noeud = f'"{self.valeur}"'
        if self.est_feuille():
            return valeur_noeud
        else:
            string_rep = ""
            base_str = valeur_noeud + " -> "
            for k in self.enfants:
                string_rep += base_str + f'"{k.valeur}"' + ";\n"
            for i in self.enfants:
                str_enf = i.liste_enfants_recursif2()
                string_rep += (str_enf + "\n") if "->" in str_enf else ''
            return string_rep[:-1]

    def graphviz_export(self, nom_fichier=None) -> str:
        """
        Cette fonction crée un fichier avec le nom 'nom_fichier' qui contient
        du code qui peut être interprété par Graphviz (moteur : 'dot').
        Je recommende de mettre '.txt' à la fin du nom du fichier pour
        le rendre lisible plus facilement.
        Ne renvoie rien.
        """
        gvzcode = "digraph tree {\n" + self.liste_enfants_recursif2() + "\n}"
        if nom_fichier is None:
            return gvzcode
        else:
            with open(nom_fichier, "w") as fichier:
                fichier.write(gvzcode)

    def repr_simple(self, n=0) -> str:
        """
        Fonction récursive d'affichage de l'arbre qui a pour racine
        l'instance courante.
        Renvoie une chaîne de caractères.
        """
        is_root = 1 if n else 0
        total = (n-1)*"  " + is_root*"└─" + str(self.valeur)
        for i in self.enfants:
            total += "\n" + i.repr_simple(n+1)
        return total

    def __repr__(self) -> str:
        """
        Fonction qui renvoie une chaîne de caractères représentant
        l'arbre ayant pour racine l'instance courante.
        """
        return self.repr_simple()


def aller_jusque(arbre, n) -> list:
    """
    Renvoie une liste de toutes les valeurs des noeuds qui précede
    un noeud ayant la valeur 'n' et ce noeud.
    """
    if arbre.valeur == n:
        return [n]
    elif arbre.est_feuille():
        return [None]
    else:
        liste = [arbre.valeur]
        for i in arbre.enfants:
            temp = aller_jusque(i, n)
            if None not in temp:
                liste += temp
        if liste == [arbre.valeur]:
            return []
        else:
            return liste

def liste_feuilles_valeurs(arbre) -> list:
    """
    Renvoie la liste des valeurs des feuilles dans l'arbre 'arbre'.
    """
    if arbre.est_feuille():
        return [arbre.valeur]
    else:
        liste = []
        for i in arbre.enfants:
            liste += liste_feuilles_valeurs(i)
        return liste

def creer_arbre_knuth(n:int) -> Noeud:
    """
    Renvoie un arbre de Knuth contenant toutes les valeurs à la même
    profondeur que 'n' et avant.
    'n' doit être un entier strictement supérieur à 0.
    """
    assert isinstance(n, int) and n>0, "n doit être un entier strictement supérieur à 0 !"
    arbre = Noeud(1)
    arbre_mobile = [arbre] # Liste de noeuds
    arbre_mobile_suivant = []
    liste_val = [1]
    while n not in liste_val:
        for k in range(len(arbre_mobile)):
            for i in liste_feuilles_valeurs(arbre_mobile[k]):
                liste = aller_jusque(arbre, i)
                for j in liste:
                    if j + arbre_mobile[k].valeur not in liste_val:
                        arbre_mobile[k].ajouter(j+arbre_mobile[k].valeur)
                        liste_val.append(j+arbre_mobile[k].valeur)
        for h in arbre_mobile:
            arbre_mobile_suivant += h.enfants
        arbre_mobile = arbre_mobile_suivant.copy()
        arbre_mobile_suivant.clear()

    return arbre