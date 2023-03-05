import pandas as pd

import src.algo2Opt
import src.geneticAlgorithm
import src.plusProcheVoisin
from src.distance import matrice_distance
from src.graph import (affichage, representation_temps_calcul)
from src.testData import data_TSPLIB, tour_optimal

# Nom des data de test
ENSEMBLE_TEST = ['ulysses22', 'att48', 'berlin52',
                 'st70', 'kroC100', 'ch150', 'gr202', 'tsp225']


def test_global_2_opt():
    """Lancement des tests de l'algorithme 2-opt

    Returns
    -------
    df_resultat_test : Dataframe 
        variable stockant un ensemble de variables importantes pour analyser
        l'algorithme
    fig_trajets : list 
        Liste des solutions des différents problèmes
    fig_temps_calcul : fig
        Figure de représentation du temps de calcul pour cet algorithme
    """
    # Dataframe à retourner, une ligne représente un test de l'algorithme
    df_resultat_test = pd.DataFrame({
        'Nombre de villes': [],
        'Solution': [],
        # Erreur par rapport à la solution optimal de la TSPLIB
        'Erreur (en %)': [],
        'Temps de calcul (en s)': []
    })
    for num_dataset in range(len(ENSEMBLE_TEST)):
        df_res, data = test_unitaire_2_opt(num_dataset)
        df_resultat_test = pd.concat(
            [df_resultat_test, df_res], ignore_index=True)

    return df_resultat_test


def test_unitaire_2_opt(num_dataset):
    """Lancement d'un test de l'algorithme 2-opt

    Returns
    -------
    Dataframe
        variable stockant un ensemble de variables importantes pour analyser
        l'algorithme
    """
    # Initialisation du data frame avec TSPLIB
    data = data_TSPLIB(f'data/{ENSEMBLE_TEST[num_dataset]}.txt')

    # Initialisation de la matrice des distances relatives
    mat_distance = matrice_distance(data)

    # Initialisation du chemin optimal
    chemin_optimal = tour_optimal(
        f'data/{ENSEMBLE_TEST[num_dataset]}_opt_tour.txt')

    # On prend un chemin initial meilleur qu'un chemin aléatoire
    # Attention cheminInitial est la liste des chemin exploré par l'algorithme
    # plus_proche_voisin
    cheminInitial, temps_calcul = src.plusProcheVoisin.plus_proche_voisin(
        data, mat_distance)

    # Lancement de l'algorithme 2-opt
    df_res = src.algo2Opt.main(mat_distance, cheminInitial[-1], chemin_optimal)
    return (df_res, data)


def test_global_plus_proche_voisin():
    """Lancement des tests de l'algorithme plus proche voisin

    Returns
    -------
    Dataframe
        variable stockant un ensemble de variables importantes pour analyser
        l'algorithme
    """
    # Dataframe à retourner, une ligne représente un test de l'algorithme
    df_resultat_test = pd.DataFrame({
        'Nombre de villes': [],
        'Solution': [],
        # Erreur par rapport à la solution optimal de la TSPLIB
        'Erreur (en %)': [],
        'Temps de calcul (en s)': []
    })

    for num_dataset in range(len(ENSEMBLE_TEST)):
        df_res, data = test_unitaire_plus_proche_voisin(num_dataset)
        df_resultat_test = pd.concat(
            [df_resultat_test, df_res], ignore_index=True)

    return (df_resultat_test)


def test_unitaire_plus_proche_voisin(num_dataset):
    """Lancement d'un test de l'algorithme du plus proche voisin

    Returns
    -------
    Dataframe
        variable stockant un ensemble de variables importantes pour analyser
        l'algorithme
    """
    # Initialisation du data frame avec TSPLIB
    data = data_TSPLIB(f'data/{ENSEMBLE_TEST[num_dataset]}.txt')

    # Initialisation de la matrice des distances relatives
    mat_distance = matrice_distance(data)

    # Initialisation du chemin optimal
    chemin_optimal = tour_optimal(
        f'data/{ENSEMBLE_TEST[num_dataset]}_opt_tour.txt')

    # Lancement de l'algorithme plus proche voisin
    df_res = src.plusProcheVoisin.main(data, mat_distance, chemin_optimal)

    return (df_res, data)


def test_global_algo_genetique():
    """Lancement des tests de l'algorithme plus proche voisin

    Returns
    -------
    Dataframe
        variable stockant un ensemble de variables importantes pour analyser
        l'algorithme
    """
    # Dataframe à retourner, une ligne représente un test de l'algorithme
    df_resultat_test = pd.DataFrame({
        'Nombre de villes': [],
        'Solution': [],
        # Erreur par rapport à la solution optimal de la TSPLIB
        'Erreur (en %)': [],
        'Temps de calcul (en s)': []
    })

    for num_dataset in range(len(ENSEMBLE_TEST)):
        df_res, data = test_unitaire_algo_genetique(num_dataset)
        df_resultat_test = pd.concat(
            [df_resultat_test, df_res], ignore_index=True)

    return (df_resultat_test)


def test_unitaire_algo_genetique(num_dataset):
    """Lancement d'un test de l'algorithme génétique

    Returns
    -------
    Dataframe
        variable stockant un ensemble de variables importantes pour analyser
        l'algorithme
    """
    # Initialisation du data frame avec TSPLIB
    data = data_TSPLIB(f'data/{ENSEMBLE_TEST[num_dataset]}.txt')

    # Initialisation de la matrice des distances relatives
    mat_distance = matrice_distance(data)

    # Initialisation du chemin optimal
    chemin_optimal = tour_optimal(
        f'data/{ENSEMBLE_TEST[num_dataset]}_opt_tour.txt')

    # Lancement de l'algorithme génétique
    df_res = src.geneticAlgorithm.main(data, mat_distance, chemin_optimal)

    return (df_res, data)
