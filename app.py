# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, Input, Output, dcc, html
from dash.dependencies import Input, Output, State

import src.algo2Opt
import src.geneticAlgorithm
import src.plusProcheVoisin
import src.testTSPLIB as testTSP
import utils.dash_reusable_components as drc
from src.distance import matrice_distance
from src.graph import affichage, representation_temps_calcul
from src.randomData import init_random_df
from src.testData import data_TSPLIB, tour_optimal

app = Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
app.title = "TSP Solver"

app.layout = html.Div(
    children=[
        html.Div(
            className="banner",
            children=[
                html.Div(
                    className="container scalable",
                    children=[
                        html.H2(
                            id="banner-title",
                            children=[
                                html.A(
                                    "Travelling Salesman Problem (TSP) Solver",
                                    href="https://github.com/Thomas-rnd/dash_TSP",
                                    style={
                                        "text-decoration": "none",
                                        "color": "inherit",
                                    },
                                )
                            ],
                        ),
                        html.A(
                            id="banner-logo",
                            children=[
                                html.Img(src=app.get_asset_url(
                                    "tsp-logo.jpg"))
                            ]
                        ),
                    ],
                )
            ],
        ),

        html.Div(
            id="body",
            className="container scalable",
            children=[
                html.Div(
                    id="app-container",
                    className="row",
                    children=[
                        html.Div(
                            className="three columns",
                            id="left-column",
                            children=[
                                drc.Card(
                                    id="first-card",
                                    children=[
                                        drc.NamedDropdown(
                                            name="Select Algorithme",
                                            id="dropdown-select-algorithm",
                                            options=[
                                                {'label': '2-opt', 'value': 0},
                                                {'label': 'Plus proche voisin',
                                                 'value': 1},
                                                {'label': 'Algorithme génétique',
                                                    'value': 2}
                                            ],
                                            clearable=False,
                                            searchable=False,
                                            value=0,
                                        ),
                                        drc.NamedDropdown(
                                            name="Select a dataset",
                                            id="dropdown-select-dataset",
                                            options=[
                                                {'label': '22- ulysses', 'value': 0},
                                                {'label': '48 - att',
                                                 'value': 1},
                                                {'label': '52 - berlin',
                                                 'value': 2},
                                                {'label': '70 - st',
                                                 'value': 3},
                                                {'label': '100 - kroC',
                                                 'value': 4},
                                                {'label': '150 - ch',
                                                 'value': 5},
                                                {'label': '202 - gr',
                                                 'value': 6},
                                                {'label': '225 - tsp', 'value': 7}
                                            ],
                                            clearable=False,
                                            searchable=False,
                                            value=0,
                                        ),
                                    ]
                                ),
                            ],
                        ),
                        dcc.Loading(html.Div(
                            id="div-graphs",
                            children=dcc.Graph(
                                id="graph-tsp",
                                figure=dict(
                                    layout=dict(
                                        plot_bgcolor="#282b38", paper_bgcolor="#282b38"
                                    )
                                ),
                            ),
                        )
                        ),
                    ],
                )
            ],
        ),
        html.Div(
            id="body",
            className="container scalable",
            children=[
                html.Div(
                    id="app-container",
                    className="row",
                    children=[
                        html.Div(
                            className="three columns",
                            id="left-column",
                            children=[
                                drc.Card(
                                    id="first-card",
                                    children=[
                                        drc.NamedDropdown(
                                            name="Select Algorithme",
                                            id="dropdown-select-algorithm-time",
                                            options=[
                                                {'label': '2-opt', 'value': 0},
                                                {'label': 'Plus proche voisin',
                                                 'value': 1},
                                                {'label': 'Algorithme génétique',
                                                    'value': 2}
                                            ],
                                            clearable=False,
                                            searchable=False,
                                            value=0,
                                        ),
                                    ]
                                ),
                            ],
                        ),
                        dcc.Loading(html.Div(
                            id="div-graphs-bis",
                            children=dcc.Graph(
                                id="graph-tsp-bis",
                                figure=dict(
                                    layout=dict(
                                        plot_bgcolor="#282b38", paper_bgcolor="#282b38"
                                    )
                                ),
                            ),
                        )
                        ),
                    ],
                )
            ],
        ),
        html.Div(
            id="body",
            className="container scalable",
            children=[
                html.Div(
                    id="app-container",
                    className="row",
                    children=[
                        html.Div(
                            className="three columns",
                            id="left-column",
                            children=[
                                drc.Card(
                                    id="first-card",
                                    children=[
                                        drc.NamedDropdown(
                                            name="Select Algorithme",
                                            id="dropdown-select-algorithm-random",
                                            options=[
                                                {'label': '2-opt', 'value': 0},
                                                {'label': 'Plus proche voisin',
                                                 'value': 1},
                                                {'label': 'Algorithme génétique',
                                                    'value': 2}
                                            ],
                                            clearable=False,
                                            searchable=False,
                                            value=0,
                                        ),
                                        drc.NamedSlider(
                                            name="Sample Size",
                                            id="slider-dataset-sample-size",
                                            min=100,
                                            max=500,
                                            step=100,
                                            marks={
                                                str(i): str(i)
                                                for i in [100, 200, 300, 400, 500]
                                            },
                                            value=300,
                                        ),
                                    ]
                                ),
                            ],
                        ),
                        dcc.Loading(html.Div(
                            id="div-graphs-random",
                            children=dcc.Graph(
                                id="graph-tsp-random",
                                figure=dict(
                                    layout=dict(
                                        plot_bgcolor="#282b38", paper_bgcolor="#282b38"
                                    )
                                ),
                            ),
                        )
                        ),
                    ],
                )
            ],
        ),
    ]
)

"""
        html.Div(id="app-container",
                 className="app-container",
                 children=[
                     html.Div(id="left-column",
                              className="left-column",
                              children=[
                                  html.H3(
                                      "Sélection d'un jeu de données aléatoire: "),
                                  dcc.Slider(50, 500, 50,
                                             value=50,
                                             id='slider-city-number'
                                             ),
                              ],),
                     html.Div(id="right-column",
                              className="right-column",
                              children=[
                                  dcc.Graph(
                                      id='graph-solution-test'),
                                  dcc.Graph(
                                      id='graph-temps-calcul-test'),
                                  dcc.Graph(
                                      id='graph-solution-random'),
                              ]),
                 ])
    ])
"""


@ app.callback(
    Output("div-graphs", "children"),
    Input('dropdown-select-dataset', 'value'),
    Input('dropdown-select-algorithm', 'value')
)
def update_data_test(num_dataset, algo):
    if algo == 0:
        df_unitaire, data = testTSP.test_unitaire_2_opt(int(num_dataset))
    elif algo == 1:
        df_unitaire, data = testTSP.test_unitaire_plus_proche_voisin(
            int(num_dataset))
    else:
        df_unitaire, data = testTSP.test_unitaire_algo_genetique(
            int(num_dataset))
    solution_figure = affichage(df_unitaire, data)
    return [
        html.Div(
            id="tsp-graph-container",
            children=dcc.Loading(
                className="graph-wrapper",
                children=dcc.Graph(id="graph-tsp",
                                   figure=solution_figure),
                style={"display": "none"},
            ),
        ),]


@ app.callback(
    Output("div-graphs-random", "children"),
    Input('slider-dataset-sample-size', 'value'),
    Input('dropdown-select-algorithm-random', 'value')
)
def update_data_test(taille_dataset, algo):
    # Initialisation du data frame avec TSPLIB
    data = init_random_df(taille_dataset)

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

    # La solution trouvée par l'algo choisi
    solution_figure = affichage(df_res, data)

    return [
        html.Div(
            id="tsp-graph-container",
            children=dcc.Loading(
                className="graph-wrapper",
                children=dcc.Graph(id="graph-tsp",
                                   figure=solution_figure),
                style={"display": "none"},
            ),
        ),]


@ app.callback(
    Output("div-graphs-bis", "children"),
    Input('dropdown-select-algorithm-time', 'value')
)
def update_data_test(algo):
    if algo == 0:
        df_global = testTSP.test_global_2_opt()
    elif algo == 1:
        df_global = testTSP.test_global_plus_proche_voisin()
    else:
        df_global = testTSP.test_global_algo_genetique()
    # Figure de représentation du temps de calcul pour un algorithme
    figure_temps_calcul = representation_temps_calcul(df_global)
    return [
        html.Div(
            id="graphs-container",
            children=[
                dcc.Loading(
                    className="graph-wrapper",
                    children=dcc.Graph(
                        id="graph-line-roc-curve", figure=figure_temps_calcul),
                ),
            ],
        ),
    ]


"""
@ app.callback(
    Output('graph-solution-random', 'figure'),
    Input('slider-city-number', 'value'),
    Input('dropdown-algo', 'value'),)
def update_random_data_test(city_number, algo):
    Lancement d'un test de l'algorithme 2-opt

 Returns
  -------
   df_res: Dataframe
     variable stockant un ensemble de variables importantes pour analyser
      l'algorithme
    fig_trajet: fig
     Solution trouvée

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
"""

# Running the server
if __name__ == '__main__':
    app.run_server(debug=True)
