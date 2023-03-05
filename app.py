# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

import src.algo2Opt
import src.geneticAlgorithm
import src.plusProcheVoisin
import src.testTSPLIB as testTSP
from src.randomData import init_random_df
from src.distance import matrice_distance
from src.graph import affichage, representation_temps_calcul
from src.testData import data_TSPLIB, tour_optimal

app = Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
app.title = "TSP Solver"

colors = {
    'background': 'white',
    'text': 'black'
}

app.layout = html.Div(style={'backgroundColor': colors['background']},
                      children=[

    html.Div(id="header",
             className="header",
             children=[
                 html.H1(
                      children='TSP Solver',
                      style={
                          'textAlign': 'center',
                          'color': colors['text']
                      }
                      ),

                 html.Div(children='Une application web permettant de tester simplement ses algorithmes de résolution du problème du voyageur de commerce',
                          style={
                              'textAlign': 'center',
                              'color': colors['text']
                          })]),

    html.Div(id="app-container",
             className="app-container",
             children=[
                html.Div(id="left-column",
                         className="left-column",
                         children=[
                             html.H3("Choix de l'algorithme : "),
                             dcc.Dropdown(options=[
                                 {'label': '2-opt', 'value': 0},
                                 {'label': 'Plus proche voisin', 'value': 1},
                                 {'label': 'Algorithme génétique', 'value': 2}],
                                 value=0, clearable=False, id='dropdown-algo'),
                            html.H3('Sélection du jeu de données : '),
                            dcc.Dropdown(options=[
                                {'label': '22- ulysses', 'value': 0},
                                {'label': '48 - att', 'value': 1},
                                {'label': '52 - berlin', 'value': 2},
                                {'label': '70 - st', 'value': 3},
                                {'label': '100 - kroC', 'value': 4},
                                {'label': '150 - ch', 'value': 5},
                                {'label': '202 - gr', 'value': 6},
                                {'label': '225 - tsp', 'value': 7}],
                                value=0, clearable=False, id='dropdown-data-test'),

                            html.H3("Sélection d'un jeu de données aléatoire: "),
                            dcc.Slider(50, 500, 50,
                                       value=50,
                                       id='slider-city-number'
                                       ),
                         ],
                         style={
                             'textAlign': 'center',
                             'color': colors['text']
                         }),
                 dcc.Graph(
                    id='graph-solution-test'),
                dcc.Graph(
                    id='graph-temps-calcul-test'),
                dcc.Graph(
                    id='graph-solution-random'),
             ])
])


@ app.callback(
    Output('graph-solution-test', 'figure'),
    Input('dropdown-data-test', 'value'),
    Input('dropdown-algo', 'value')
)
def update_data_test(num_dataset, algo):
    if algo == 0:
        df, data = testTSP.test_unitaire_2_opt(int(num_dataset))
    elif algo == 1:
        df, data = testTSP.test_unitaire_plus_proche_voisin(int(num_dataset))
    else:
        df, data = testTSP.test_unitaire_algo_genetique(int(num_dataset))
    fig = affichage(df, data)
    return (fig)


@ app.callback(
    Output('graph-temps-calcul-test', 'figure'),
    Input('dropdown-algo', 'value')
)
def update_temps_calcul(algo):
    if algo == 0:
        df = testTSP.test_global_2_opt()
    elif algo == 1:
        df = testTSP.test_global_plus_proche_voisin()
    else:
        df = testTSP.test_global_algo_genetique()

    # Figure de représentation du temps de calcul pour un algorithme
    fig_temps_calcul = representation_temps_calcul(df)
    return (fig_temps_calcul)


@ app.callback(
    Output('graph-solution-random', 'figure'),
    Input('slider-city-number', 'value'),
    Input('dropdown-algo', 'value'),)
def update_random_data_test(city_number, algo):
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
    data = init_random_df(city_number)

    # Initialisation de la matrice des distances relatives
    mat_distance = matrice_distance(data)

    if algo == 0:
        # On prend un chemin initial meilleur qu'un chemin aléatoire
        # Attention cheminInitial est la liste des chemin exploré par l'algorithme
        # plus_proche_voisin
        cheminInitial, temps_calcul = src.plusProcheVoisin.plus_proche_voisin(
            data, mat_distance)

        # Lancement de l'algorithme 2-opt
        df_res = src.algo2Opt.main(
            mat_distance, cheminInitial[-1])
    elif algo == 1:
        # Lancement de l'algorithme plus proche voisin
        df_res = src.plusProcheVoisin.main(data, mat_distance)
    else:
        df_res = src.geneticAlgorithm.main(data, mat_distance)

    # Liste des solutions des différents problèmes
    fig_trajet = affichage(df_res, data)

    return fig_trajet


if __name__ == '__main__':
    app.run_server(debug=True)
