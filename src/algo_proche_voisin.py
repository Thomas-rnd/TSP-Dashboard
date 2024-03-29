import time

import numpy as np
import pandas as pd

from src.distance import distance_trajet

# Implémentation de l'algorithme du 1-plus proche voisin adapté à la résolution
# du TSP. C'est un algorithme simple afin d'obtenir très rapidement une solution
# approximative et non aléatoire au problème.

# Cf. : https://fr.wikipedia.org/wiki/Recherche_des_plus_proches_voisins


def plus_proche_voisin(matrice_distance: np.ndarray) -> tuple[list[int], float, list[list[int]]]:
    """Retourne le trajet trouvé en se déplacement de proche en proche.

    La ville de départ étant arbitraire on choisit la ville d'index 0

    Parameters
    ----------
    matrice_distance : np.array
        matrice stockant l'integralité des distances inter villes

    Returns
    -------
    itineraire : list[int]
        le chemin finalement trouvé
    temps_calcul : float
        temps necessaire à la résolution du problème
    """
    start_time = time.time()

    # Initialiation d'une matrice booléenne d'état de visite des villes
    visite = np.zeros(len(matrice_distance)) != 0

    # Initialisation de l'itinéraire
    itineraire = [0]
    visite[0] = True

    while False in visite:
        # A chaque itération on cherche la ville la plus proche de la ville actuelle
        # la ville actuelle étant la dernière de l'itinéraire

        # Pour ne pas modifier les valeurs de matrice_distance
        distance_a_ville = np.copy(matrice_distance[itineraire[-1], :])

        for index in range(len(distance_a_ville)):
            if visite[index]:
                distance_a_ville[index] = np.Inf

        # Récupération de l'index de la ville la plus proche
        plus_proche = np.argmin(distance_a_ville)

        # On donne l'état visité à la ville la plus proche
        visite[plus_proche] = True

        itineraire.append(int(plus_proche))

    # On pense à fermer le cycle
    itineraire.append(itineraire[0])

    temps_calcul = time.time() - start_time
    return itineraire, temps_calcul


def main(matrice_distance: np.ndarray, nom_dataset="") -> tuple[pd.DataFrame, list[list[int]]]:
    """Lancement de l'algorithme de recherche 

    Parameters
    ----------
    matrice_distance : np.array
        matrice stockant l'integralité des distances inter villes
    nom_dataset : str (optionnel)
        Nom du dataset à traiter

    Returns
    -------
    Dataframe
        variable stockant un ensemble de variables importantes pour analyser
        l'algorithme
    """
    # Résolution du TSP
    itineraire, temps_calcul = plus_proche_voisin(
        matrice_distance)

    # Calcul de la distance du trajet final trouvé par l'algorithme
    distance_chemin_sub_optimal = distance_trajet(itineraire, matrice_distance)

    # Création du dataframe à retourner
    # On inclut pas les chemins explorés pour pas sucharger le fichier csv de résultats
    df_resultat_test = pd.DataFrame({
        'Algorithme': "plus_proche_voisin",
        'Nom dataset': nom_dataset,
        'Nombre de villes': len(itineraire)-1,
        # Dans un tableau pour être sur une seule ligne du dataframe
        'Solution': [itineraire],
        'Distance': distance_chemin_sub_optimal,
        'Temps de calcul (en s)': temps_calcul
    })

    return df_resultat_test
