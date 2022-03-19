#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "main.h"

#define TAILLE_MOT_MAX 100
#define NOMBRE_DE_VIES 10 // 7 Par défaut

/* TODO :
    ->Play-testing
*/

int main(int argc, char *argv[])
{
    srand(time(NULL));
    FILE* fichier = NULL;
    char nb_ligne_str[TAILLE_MOT_MAX];
    char mot_secret[TAILLE_MOT_MAX] = "TEST";
    char lettre_joueur;
    char lettres_essaye[50]; // plus de 26 caractere sont prevus au cas ou l'utilisateur utilise autre chose que des lettres
    char mot_affiche[TAILLE_MOT_MAX];
    int vies = NOMBRE_DE_VIES;
    int nb_ligne;
    int indice_mot = 0;
    int incr_lettres_essaye = 0;

    memset(lettres_essaye, 0, 50); // On vide le tableau lettre_essaye

    fichier = fopen("dico.dict", "r");
    if (fichier==NULL)
    {
      printf("Le dictionnaire n'a pas ete trouve !");
      return -1;
    }
    fgets(nb_ligne_str, 10, fichier);
    sscanf(nb_ligne_str, "%i", &nb_ligne); // nb_ligne -> Nombre de mot dans le dictionnaire
    for (int y=0; y<((nb_ligne/RAND_MAX)+1); y++)
    {
        indice_mot += rand(); // Pour le choix du mot secret
    }

    rewind(fichier);
    int y = 0;
    while (fgets(nb_ligne_str, TAILLE_MOT_MAX, fichier))
    {
        y++;
        if (y == indice_mot)
        {
            strcpy(mot_secret, strupr(nb_ligne_str));
            mot_secret[strlen(mot_secret)-1] = '\0';
            break;
        }
    }


    fclose(fichier);

    strcpy(mot_affiche, mot_secret); // mot_affiche -> "TEST"
    mettreAJourMot(mot_secret, mot_affiche, lettres_essaye); // mot_affiche -> "****"


    // Boucle principal du jeu :
    printf("Trouvez le mot secret ou perissez !");
    while (strcmp(mot_secret, mot_affiche) && (vies != 0))
    {
        printf("\nLe mot secret pour l'instant : %s", mot_affiche);
        printf("\nLettre essayee : %s", lettres_essaye);
        printf("\nVous avez %i vies restantes : ", vies);
        lettre_joueur = lireCaractere();
        if (strchr(lettres_essaye, lettre_joueur) != NULL)
        {
            printf("\nLettre deja utilisee... Essayez une autre !");
        }
        else
        {
            lettres_essaye[incr_lettres_essaye] = lettre_joueur;
            incr_lettres_essaye++;
            if (strchr(mot_secret, lettre_joueur) == NULL)
            {
                printf("\nLa lettre n'etait pas dans le mot. -1 point de vie !");
                vies--;
            }
            else
            {
                mettreAJourMot(mot_secret, mot_affiche, lettres_essaye);
            }
        }
        tri_tableau_char(lettres_essaye, 50);
    }
    if (vies == 0)
    {
        printf("\nVous etes mort ! Vous avez perdu.\nLe mot etait : %s\n", mot_secret);
    }
    else
    {
        printf("\nVous avez gagne ! Le mot secret etait : %s\n", mot_secret);
    }
    printf("\n\nFin de la partie, pour quitter appuyer sur entre.");
    lireCaractere();

    return 0;
}

// Sorte de tri surprise modifié :
void tri_tableau_char(char tableau[], int taille_tableau)
{
    char temp;
    for (int i=1; i!=taille_tableau; i++)
    {
        for (int j=0; j!=i; j++)
        {
            if ((tableau[i] < tableau[j]) && (tableau[j] != 0) && (tableau[i] != 0))
            {
                temp = tableau[j];
                tableau[j] = tableau[i];
                tableau[i] = temp;
                // printf("\nDEBUG TRI2 : %s, %c, %c\n", tableau, tableau[i], tableau[j]); // DEBUG
            }
        }
    }
}

// Permet de lire UN caractere donne par le joueur :
char lireCaractere()
{
    char caractere = 0;
    caractere = getchar();
    caractere = toupper(caractere);

    while (getchar() != '\n');

    return caractere;
}

// Retire les lettres qui n'ont pas ete essaye dans le mot secret pour le montrer au joueur :
void mettreAJourMot(char mot_cache[], char mot_motif[], char lettres_essaye[])
{
    int compteur = 0;
    strcpy(mot_motif, mot_cache);
        while (mot_motif[compteur] != '\0')
    {
        if (strchr(lettres_essaye, mot_cache[compteur]) == NULL)
        {
            mot_motif[compteur] = '*';
            // printf("%s \n", mot_motif); // DEBUG
        }
        compteur++;
    }
}
