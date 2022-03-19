import tkinter as tk
import math
from typing import Union, List, Dict, Tuple

__author__ = "Gabriel Dosne"

# Commandes recommandées :
#   GRAPHE.affiche_graphe_interactif()
#   GRAPHE possible -> graphe0, graphe1, graphe2, graphe3,
#                      graphe4, graphe_complet4, graphe_complet7

class Sommet:
    def __init__(self, nom: str, donnee: str=None):
        self.nom = nom
        self.donnee = donnee if donnee is not None else self.nom

    def get_donnee(self) -> str:
        """
        Renvoie l'attribut 'donnee' de l'instance courante.
        """
        return self.donnee

    def set_donnee(self, donnee: str) -> None:
        """
        Définie l'attribut 'donnee' de l'instance courante
        avec la valeur entrée en paramètre.
        Ne renvoie rien.
        """
        self.donnee = donnee

    def __eq__(self, other) -> bool:
        """
        Égalité : Deux instances de Sommet sont égalent si
        leurs attributs sont égaux.
        """
        return (self.nom, self.donnee) == (other.nom, other.donnee)

    def __hash__(self) -> int:
        """
        Renvoie la valeur du hash du 2-uplet
        des attributs de l'instance courante.
        (La méthode est définie pour pouvoir utiliser
        une instance de Sommet comme clef de dictionnaire)
        """
        return hash((self.nom, self.donnee))

    def __repr__(self) -> str:
        """
        Renvoie la représentation canonique en chaîne de
        caractères de l'instance courante.
        (C'est-à-dire que :
        eval(repr(obj)) == obj)
        """
        return f"Sommet('{self.nom}', '{self.donnee}')"

class Arete:
    def __init__(self, sommet: set, coefficient: Union[float, int]=None, origine: Sommet=None, extremite: Sommet=None):
        self.sommet = sommet
        self.coefficient = coefficient
        self.origine = origine
        self.extremite = extremite

    def get_coefficient(self) -> Union[float, int]:
        """
        Renvoie l'attribut 'coefficient' de l'instance courante.
        """
        return self.coefficient

    def set_coefficient(self, coefficient: Union[float, int]) -> None:
        """
        Définie l'attribut 'coefficient' de l'instance courante
        avec la valeur entrée en paramètre.
        Ne renvoie rien.
        """
        self.coefficient = coefficient

    def __repr__(self) -> str:
        """
        Renvoie la représentation canonique en chaîne de
        caractères de l'instance courante.
        (C'est-à-dire que :
        eval(repr(obj)) == obj)
        """
        return f"Arete({self.sommet}, {self.coefficient}, {self.origine}, {self.extremite})"

class Graphe:
    def __init__(self, sommets: List[Sommet]=None, aretes: List[Arete]=None, oriente: bool=False, pondere: bool=False):
        self.sommets = sommets if sommets is not None else list()
        self.aretes = aretes if aretes is not None else list()
        self.oriente = oriente
        self.pondere = pondere
        if not self.pondere:
            for i in self.aretes:
                i.set_coefficient("1")

    def get_arete(self) -> List[Arete]:
        """
        Renvoie l'attribut 'aretes' de l'instance courante.
        """
        return self.aretes

    def ajoute_arete(self, arete: Tuple[Sommet, Sommet, Union[int, float]]) -> None:
        """
        Ajoute une arête au graphe.
        Le paramètre 'arete' est un 2-uplet
        (ou 3-uplet si le graphe est pondéré).
        Il suit ce format :
        (origine: Sommet, fin: Sommet, ponderation: Union[float, int])
        Ne renvoie rien.
        """
        ponderation = arete[-1] if self.pondere else "1"
        origine, extremite = (arete[0], arete[1]) if self.oriente else (None, None)
        new_arete = Arete({arete[0], arete[1]}, ponderation, origine, extremite)
        self.aretes.append(new_arete)

    def get_sommet(self) -> List[Sommet]:
        """
        Renvoie l'attribut 'sommets' de l'instance courante.
        """
        return self.sommets

    def ajoute_sommet(self, sommet: Sommet) -> None:
        """
        Ajoute un sommet au graphe.
        Le paramètre 'sommet' est une
        instance de la classe Sommet.
        Ne renvoie rien.
        """
        self.sommets.append(sommet)

    def est_complet(self) -> bool:
        """
        Renvoie True si le graphe est complet et False sinon.
        """
        coef_est_oriente = 2 if self.oriente else 1
        return len(self.aretes) == sum(range(1, len(self.sommets)))*coef_est_oriente

    def affiche_graphe(self, dim: int=700) -> None:
        """
        Affiche le graphe avec Tkinter.
        La taille de la fenêtre en pixel est de 'dim'*'dim'.
        Ne renvoie rien.
        """
        offset = int(math.sqrt((dim/2)*(dim/2)))
        padding = 40
        circle_size = 20
        window = tk.Tk()
        canvas = tk.Canvas(window, width=dim, height=dim)
        coef_offset_base = 30 # Pour graphe orienté
        # canvas.create_oval(padding, padding, dim-padding, dim-padding) # Cercle sur lequel on mets les sommets

        dist_degr = int(360/len(self))
        dico_pos = {i: (dim-padding, offset) for i in self.get_sommet()}
        for j, somm in enumerate(dico_pos):
            temp_x, temp_y = dico_pos[somm]
            rotation = math.radians((j+1)*dist_degr)
            rot_x = ((temp_x-offset) * math.cos(rotation)) + ((temp_y-offset) * math.sin(rotation)) + offset
            rot_y = (-(temp_x-offset) * math.sin(rotation)) + ((temp_y-offset) * math.cos(rotation)) + offset
            dico_pos[somm] = (rot_x, rot_y)

        liste_coord = []
        liste_sommet_deja_vu = [] if self.oriente else None

        for k in self.get_arete():
            coord = (k.origine, k.extremite) if self.oriente else tuple(k.sommet)
            if self.oriente:
                liste_sommet_deja_vu.append((k.origine, k.extremite))
                vecteur_orig_extr = (dico_pos[coord[0]][0]-dico_pos[coord[1]][0], dico_pos[coord[0]][1]-dico_pos[coord[1]][1])
                coef_ajustement = circle_size/math.sqrt(vecteur_orig_extr[0]**2 + vecteur_orig_extr[1]**2)
                vecteur_ajuste = (coef_ajustement*vecteur_orig_extr[0], coef_ajustement*vecteur_orig_extr[1])
                a_prime = (dico_pos[coord[0]][0]-vecteur_ajuste[0], dico_pos[coord[0]][1]-vecteur_ajuste[1])
                b_prime = (dico_pos[coord[1]][0]+vecteur_ajuste[0], dico_pos[coord[1]][1]+vecteur_ajuste[1])
                vecteur_normal = (-vecteur_orig_extr[1], vecteur_orig_extr[0])
                coef_normal_ajustement = coef_offset_base/math.sqrt(vecteur_normal[0]**2 + vecteur_normal[1]**2)
                vecteur_normal_ajuste = (coef_normal_ajustement*vecteur_normal[0], coef_normal_ajustement*vecteur_normal[1])
                milieu_offset = (((a_prime[0]+b_prime[0])/2)+vecteur_normal_ajuste[0]*2, ((a_prime[1]+b_prime[1])/2)+vecteur_normal_ajuste[1]*2)
                canvas.create_line(a_prime[0], a_prime[1], milieu_offset[0], milieu_offset[1], b_prime[0], b_prime[1], smooth=True, width=2, arrow="last", arrowshape=(10, 15, 5))
            else:
                canvas.create_line(dico_pos[coord[0]][0], dico_pos[coord[0]][1], dico_pos[coord[1]][0], dico_pos[coord[1]][1], width=2)
            if self.pondere:
                if not self.oriente:
                    milieu_offset = ((dico_pos[coord[0]][0]+dico_pos[coord[1]][0])/2, (dico_pos[coord[0]][1]+dico_pos[coord[1]][1])/2)
                    vecteur_normal_ajuste = (0, 0)
                liste_coord.append((milieu_offset[0]-vecteur_normal_ajuste[0], milieu_offset[1]-vecteur_normal_ajuste[1], str(k.coefficient)))

        if self.pondere:
            coeff_circle = circle_size//2 + 3
            for m in liste_coord:
                canvas.create_oval(m[0]-coeff_circle, m[1]-coeff_circle, m[0]+coeff_circle, m[1]+coeff_circle, fill="white")
                canvas.create_text(m[0], m[1], text=m[2])

        for f in dico_pos:
            canvas.create_oval(dico_pos[f][0]-circle_size, dico_pos[f][1]-circle_size, dico_pos[f][0]+circle_size, dico_pos[f][1]+circle_size, fill="white")
            canvas.create_text(dico_pos[f][0], dico_pos[f][1], text=str(f.nom))

        canvas.pack()
        tk.mainloop()

    def affiche_graphe_interactif(self, dim: int=700) -> None:
        """
        Affiche le graphe avec Tkinter.
        On peut déplacer un sommet en
        cliquant dessus et en le faisant glisser.
        La taille de la fenêtre en pixel est de 'dim'*'dim'.
        Ne renvoie rien.
        """
        objet_select = None
        offset = int(math.sqrt((dim/2)*(dim/2)))
        padding = 40
        circle_size = 20
        window = tk.Tk()
        canvas = tk.Canvas(window, width=dim, height=dim)
        coef_offset_base = 30 # Pour graphe orienté
        # canvas.create_oval(padding, padding, dim-padding, dim-padding) # Cercle sur lequel on mets les sommets

        dist_degr = int(360/len(self))
        dico_pos = {i: (dim-padding, offset) for i in self.get_sommet()}
        for j, somm in enumerate(dico_pos):
            temp_x, temp_y = dico_pos[somm]
            rotation = math.radians((j+1)*dist_degr)
            rot_x = ((temp_x-offset) * math.cos(rotation)) + ((temp_y-offset) * math.sin(rotation)) + offset
            rot_y = (-(temp_x-offset) * math.sin(rotation)) + ((temp_y-offset) * math.cos(rotation)) + offset
            dico_pos[somm] = (rot_x, rot_y)

        pos_sommet = {pos: sommet for sommet, pos in dico_pos.items()}
        def draw(self, dico_pos: Dict[Sommet, Tuple[Union[int, float], Union[int, float]]], canvas: tk.Canvas, coef_offset_base: int) -> None:
            """
            Étant donné un dictionnaire des positions des sommets,
            la fonction dessine le graphe en remplissant le 'canvas'.
            """
            liste_coord = []
            liste_sommet_deja_vu = [] if self.oriente else None
            for k in self.get_arete():
                coord = (k.origine, k.extremite) if self.oriente else tuple(k.sommet)
                if self.oriente:
                    liste_sommet_deja_vu.append((k.origine, k.extremite))
                    vecteur_orig_extr = (dico_pos[coord[0]][0]-dico_pos[coord[1]][0], dico_pos[coord[0]][1]-dico_pos[coord[1]][1])
                    coef_ajustement = circle_size/math.sqrt(vecteur_orig_extr[0]**2 + vecteur_orig_extr[1]**2)
                    vecteur_ajuste = (coef_ajustement*vecteur_orig_extr[0], coef_ajustement*vecteur_orig_extr[1])
                    a_prime = (dico_pos[coord[0]][0]-vecteur_ajuste[0], dico_pos[coord[0]][1]-vecteur_ajuste[1])
                    b_prime = (dico_pos[coord[1]][0]+vecteur_ajuste[0], dico_pos[coord[1]][1]+vecteur_ajuste[1])
                    vecteur_normal = (-vecteur_orig_extr[1], vecteur_orig_extr[0])
                    coef_normal_ajustement = coef_offset_base/math.sqrt(vecteur_normal[0]**2 + vecteur_normal[1]**2)
                    vecteur_normal_ajuste = (coef_normal_ajustement*vecteur_normal[0], coef_normal_ajustement*vecteur_normal[1])
                    milieu_offset = (((a_prime[0]+b_prime[0])/2)+vecteur_normal_ajuste[0]*2, ((a_prime[1]+b_prime[1])/2)+vecteur_normal_ajuste[1]*2)
                    canvas.create_line(a_prime[0], a_prime[1], milieu_offset[0], milieu_offset[1], b_prime[0], b_prime[1], smooth=True, width=2, arrow="last", arrowshape=(10, 15, 5))
                else:
                    canvas.create_line(dico_pos[coord[0]][0], dico_pos[coord[0]][1], dico_pos[coord[1]][0], dico_pos[coord[1]][1], width=2)
                if self.pondere:
                    if not self.oriente:
                        milieu_offset = ((dico_pos[coord[0]][0]+dico_pos[coord[1]][0])/2, (dico_pos[coord[0]][1]+dico_pos[coord[1]][1])/2)
                        vecteur_normal_ajuste = (0, 0)
                    liste_coord.append((milieu_offset[0]-vecteur_normal_ajuste[0], milieu_offset[1]-vecteur_normal_ajuste[1], str(k.coefficient)))
            if self.pondere:
                coeff_circle = circle_size//2 + 3
                for m in liste_coord:
                    canvas.create_oval(m[0]-coeff_circle, m[1]-coeff_circle, m[0]+coeff_circle, m[1]+coeff_circle, fill="white")
                    canvas.create_text(m[0], m[1], text=m[2])
            for f in dico_pos:
                canvas.create_oval(dico_pos[f][0]-circle_size, dico_pos[f][1]-circle_size, dico_pos[f][0]+circle_size, dico_pos[f][1]+circle_size, fill="white")
                canvas.create_text(dico_pos[f][0], dico_pos[f][1], text=str(f.nom))

        def action_clic_souris(event) -> None:
            """
            Permet de 'sélectionner' un sommet
            quand l'utilisateur clique dessus.
            """
            nonlocal objet_select
            nonlocal pos_sommet
            dist = lambda x, y: math.sqrt((x[0]-y.x)**2 + (x[1]-y.y)**2) # x -> 2-uplet ; y -> event
            plus_proche = min([(dist(i, event), i) for i in pos_sommet], key=lambda x: x[0])
            if plus_proche[0] < circle_size+3:
                objet_select = pos_sommet[plus_proche[1]]
            else:
                objet_select = None

        def deplacer_widget(event) -> None:
            """
            Permet de déplacer le sommet 'sélectionné'.
            (Avec action_clic_souris)
            """
            nonlocal objet_select
            nonlocal dico_pos
            nonlocal pos_sommet
            if objet_select is not None:
                dico_pos[objet_select] = (event.x, event.y)
                pos_sommet = {pos: sommet for sommet, pos in dico_pos.items()}
                canvas.delete("all")
                draw(self, dico_pos, canvas, coef_offset_base)

        draw(self, dico_pos, canvas, coef_offset_base)
        canvas.pack()
        canvas.bind("<Button-1>", action_clic_souris)
        canvas.bind("<B1-Motion>", deplacer_widget)
        tk.mainloop()

    def __len__(self) -> int:
        """
        Renvoie le nombre de sommet du graphe.
        """
        return len(self.sommets)

    def __repr__(self) -> str:
        """
        Renvoie la représentation canonique en chaîne de
        caractères de l'instance courante.
        (C'est-à-dire que :
        eval(repr(obj)) == obj)
        """
        return f"Graphe({self.sommets}, {self.aretes}, {self.oriente}, {self.pondere})"


def generer_graphe_complet_dict(n: int=3) -> Dict[str, List[str]]:
    """
    Génére un graphe complet avec 'n' sommets numérotés de 1 à 'n'.
    (Sous forme d'un dictionnaire).
    """
    return {str(i):[str(j) for j in range(1, n+1) if j != i] for i in range(1, n+1)}

def tous_les_couplages(dico: Dict[str, List[str]], oriente: bool=False, ponderation: Dict[Tuple[str, str], Union[int, float]]=None, donnees: Dict[str, str]=None) -> List[Arete]:
    """
    Génére une liste d'arêtes étant donné un dictionnaire de graphe,
    s'il est orienté ou non,
    le coefficient de pondération pour chaque couples de sommets et
    les données associées à chaque sommets.
    Renvoie une liste d'arêtes de type Arete.
    """
    ponderation = dict() if ponderation is None else ponderation
    donnees = dict() if donnees is None else donnees
    liste_aretes = []
    liste_deja_ut = []
    for i in dico:
        for j in dico[i]:
            if oriente or (j not in liste_deja_ut):
                liste_aretes.append(Arete({Sommet(str(i), donnees.get(i, None)), Sommet(str(j), donnees.get(i, None))}, ponderation.get((i,j), 1), Sommet(str(i), donnees.get(i, None)), Sommet(str(j), donnees.get(i, None))))
        liste_deja_ut.append(i)
    return liste_aretes

def dico_vers_graphe(dico: Dict[str, List[str]], oriente: bool=False, ponderation: Dict[Tuple[str, str], Union[int, float]]=None, donnees: Dict[str, str]=None) -> Graphe:
    """
    Génére un graphe du type Graphe étant donné un dictionnaire de graphe,
    s'il est orienté ou non,
    le coefficient de pondération pour chaque couples de sommets et
    les données associées à chaque sommets.
    Renvoie une instance de Graphe.
    """
    ponderation = dict() if ponderation is None else ponderation
    donnees = dict() if donnees is None else donnees
    liste_sommet = [Sommet(str(i), donnees.get(i, None)) for i in dico]
    aretes = tous_les_couplages(dico, oriente, ponderation, donnees)
    return Graphe(liste_sommet, aretes, oriente, ponderation!={})

dico1 = {"A":["B", "C", "D"], "B":["A", "C", "E"], "C":["A", "B", "D"], "D":["A", "C", "E", "F"], "E":["B", "D"], "F":["D"], "G":["A"]}

dico2 = {"A":["B"], "B":["A", "C"], "C":["B"]}

dico3 = {"A":["B", "C"], "B":["A", "C"], "C":["A", "B", "D"], "D":["C", "E", "F"], "E":["D", "F"], "F":["D", "E"]}

graphe0 = Graphe([Sommet("A", 0), Sommet("B", 1)], [Arete({Sommet("A", 0), Sommet("B", 1)}, 1.5, Sommet("A", 0), Sommet("B", 1))], True, True)
graphe1 = dico_vers_graphe(dico1, True)
graphe2 = dico_vers_graphe(dico2, True)
graphe3 = dico_vers_graphe(dico3, True)
graphe_complet4 = dico_vers_graphe(generer_graphe_complet_dict(6), True, {(str(i), str(j)): (i%2 + j/2 + 1) for i, j in list(zip(6*[1,2,3,4,5,6], 6*[1]+6*[2]+6*[3]+6*[4]+6*[5]+6*[6]))})
graphe_complet7 = dico_vers_graphe(generer_graphe_complet_dict(7))

graphe4 = Graphe([], [], False, True)
graphe4.ajoute_sommet(Sommet("D"))
graphe4.ajoute_sommet(Sommet("A"))
graphe4.ajoute_sommet(Sommet("C"))
graphe4.ajoute_sommet(Sommet("B"))
graphe4.ajoute_sommet(Sommet("F"))
graphe4.ajoute_sommet(Sommet("E"))
graphe4.ajoute_arete((Sommet("A"), Sommet("B"), 2))
graphe4.ajoute_arete((Sommet("A"), Sommet("C"), 3))
graphe4.ajoute_arete((Sommet("A"), Sommet("D"), 4))
graphe4.ajoute_arete((Sommet("A"), Sommet("E"), 2))
graphe4.ajoute_arete((Sommet("F"), Sommet("B"), 1))
graphe4.ajoute_arete((Sommet("F"), Sommet("E"), 6))
