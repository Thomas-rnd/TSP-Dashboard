# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

import src.algo2Opt
import src.geneticAlgorithm
import src.plusProcheVoisin
import src.testTSPLIB as testTSP
from src.distance import matrice_distance
from src.graph import affichage, representation_temps_calcul
from src.testData import data_TSPLIB, tour_optimal


def test_2_opt(nom_fichier):
    """Lancement d'un test de l'algorithme 2-opt

    Returns
    -------
    df_res : Dataframe
        variable stockant un ensemble de variables importantes pour analyser
        l'algorithme
    fig_trajet : fig
        Solution trouvée
    """
    # Initialisation du data frame avec TSPLIB
    data = data_TSPLIB(f'data/{nom_fichier}.txt')

    # Initialisation de la matrice des distances relatives
    mat_distance = matrice_distance(data)

    # Initialisation du chemin optimal
    chemin_optimal = tour_optimal(f'data/{nom_fichier}_opt_tour.txt')

    # On prend un chemin initial meilleur qu'un chemin aléatoire
    # Attention cheminInitial est la liste des chemin exploré par l'algorithme
    # plus_proche_voisin
    cheminInitial, temps_calcul = src.plusProcheVoisin.plus_proche_voisin(
        data, mat_distance)

    # Lancement de l'algorithme 2-opt
    df_res = src.algo2Opt.main(
        mat_distance, cheminInitial[-1], chemin_optimal)

    # Liste des solutions des différents problèmes
    fig_trajet = affichage(df_res, data)

    return (df_res, fig_trajet)


app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

df_res, fig_trajet = test_2_opt('ch150')

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for your data.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure=fig_trajet
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
