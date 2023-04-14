import glob
import os

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.init_test_data import data_TSPLIB, normalisation, trajet_en_df

# Chemin de stockage des différents fichiers numériques
# On retrouve dans ce dossier l'ensemble des figures crées
ROOT = "resultats/figures/"


def representation_itineraire_web(data: pd.DataFrame, chemins: pd.DataFrame, nom_fichier="") -> go.Figure:
    """Affichage des N villes par des points ainsi que le parcours réalisé
       Le parcours est donné par l'ordre des villes dans le dataframe

    Parameters
    ----------
    data : DataFrame
        dataframe stockant l'intégralité des coordonnées des villes à parcourir

    Returns
    -------
    Figure
        Graphique de visualisation plolty
    """
    # Affichage des villes
    fig = px.scatter(data, x='x', y='y', template="simple_white",
                     title="Shortest path found by the algorithm")

    # On relie les villes dans le bon ordre
    fig.add_trace(
        go.Scatter(
            x=chemins['x'].values,
            y=chemins['y'].values,
            mode='lines',
            showlegend=False)

    )
    fig.update_xaxes(zeroline=False, visible=False)
    fig.update_yaxes(zeroline=False, visible=False)
    return fig

def representation_temps_calcul(fichier_csv: str) -> go.Figure:
    """Affichage du temps de calcul des différents algorithmes implémentés
    en fonction du nombre de villes à parcourir.

    Parameters
    ----------
    fichier_csv : str
        fichier csv stockant l'intégralité des résultats des différents algorithmes

    Returns
    -------
    Figure
        Graphique de visualisation plolty
    """
    # Lecture du fichier stockant l'ensemble des résultats
    data = pd.read_csv(fichier_csv)
    fig = px.line(data, x='Nombre de villes',
                  y='Temps de calcul (en s)', color='Algorithme', template='plotly_white',
                  title='Representation of the calculation time according to the number of cities to explore', markers=True, log_y=True,
                  labels={"Nombre de villes": "Number of cities", "Temps de calcul (en s)": "Calculation time (in s)",
                          "Algorithme": 'Algorithm'})

    newnames = {'2-opt': '2-opt inversion', 'plus_proche_voisin': 'Nearest neighbor search',
                'genetique': 'Genetic algorithm', 'kohonen': 'Kohonen algorithm'}
    fig.for_each_trace(lambda t: t.update(name=newnames[t.name],
                                          legendgroup=newnames[t.name],
                                          hovertemplate=t.hovertemplate.replace(
        t.name, newnames[t.name])
    ))
    return fig


def representation_resultats(fichier_csv: str) -> go.Figure:
    """Affichage des distances des chemins trouvés par algorithme

    Parameters
    ----------
    fichier_csv : str
        fichier csv stockant l'intégralité des résultats des différents algorithmes

    Returns
    -------
    Figure
        Graphique de visualisation plolty
    """
    # Lecture du fichier stockant l'ensemble des résultats
    data = pd.read_csv(fichier_csv)

    fig = px.box(data, x="Algorithme", y="Distance", color="Algorithme", template='plotly_white',
                 title="Distance of the path found according to the algorithm", points="all",
                 category_orders={'Algorithme': ['2-opt inversion', 'Nearest neighbor search',
                                                 'Genetic algorithm', 'Kohonen algorithm']},
                 labels={"Nombre de villes": "Number of cities", "Temps de calcul (en s)": "Calculation time (in s)",
                         "Algorithme": 'Algorithm', "Génétique": 'Genetic'}
                 )

    newnames = {'2-opt': '2-opt inversion', 'plus_proche_voisin': 'Nearest neighbor search',
                'genetique': 'Genetic algorithm', 'kohonen': 'Kohonen algorithm'}
    fig.for_each_trace(lambda t: t.update(name=newnames[t.name],
                                          legendgroup=newnames[t.name],
                                          hovertemplate=t.hovertemplate.replace(
        t.name, newnames[t.name])
    )
    )
    return fig


def affichage(df_resolution: pd.DataFrame, data: pd.DataFrame, nom_fichier="") -> go.Figure:
    """Affichage d'un trajet et des performances d'un algorithme

    Parameters
    ----------
    df_resolution : Dataframe
        variable stockant un ensemble de variables importantes pour analyser
        l'algorithme
    data : DataFrame
        dataframe stockant l'intégralité des coordonnées des villes à parcourir
    nom_fichier : str (optionnel)
        nom du fichier si on souhaite sauvegarder la figure crée

    Returns
    -------
    Figure
        Graphique de visualisation plolty
    """
    # Création d'un dataframe complet issu de la solution trouvée
    df_meilleur_trajet = trajet_en_df(
        df_resolution['Solution'][0], data)
    # Création de la figure avec sauvegarde
    if nom_fichier != "":
        fig = representation_itineraire_web(
            data, df_meilleur_trajet, f"{ROOT+nom_fichier}.png")
    # Création de la figure sans sauvegarde
    else:
        fig = representation_itineraire_web(
            data, df_meilleur_trajet)

    # Affichage console de certain résultat
    # print("=============================================")
    # print("Nombre de ville : ", df_resolution["Nombre de villes"][0])
    # print("Distance : ", df_resolution["Distance"][0])
    # print("Temps de calcul (en s): ",
    #      df_resolution["Temps de calcul (en s)"][0])
    # print("=============================================")
    return fig