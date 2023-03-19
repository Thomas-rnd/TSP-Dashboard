# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import plotly.express as px
from dash import Dash, Input, Output, ctx, dcc, html
from dash.dependencies import Input, Output, State

import src.algo_2_opt
import src.algo_genetique
import src.algo_proche_voisin
import src.test_algo
import utils.dash_reusable_components as drc
from src.distance import matrice_distance
from src.affichage_resultats import affichage
from src.init_random_data import init_random_df

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
                    children=[
                        html.Div(
                            id="left-column",
                            children=[
                                drc.Card(
                                    id="first-card",
                                    children=[
                                        drc.NamedDropdown(
                                            name="Select Algorithm",
                                            id="dropdown-select-algorithm",
                                            options=[
                                                {'label': '2-opt inversion',
                                                    'value': 0},
                                                {'label': 'Nearest neighbor search',
                                                 'value': 1},
                                                {'label': 'Genetic algorithm',
                                                    'value': 2}
                                            ],
                                            clearable=False,
                                            searchable=False,
                                            value=0,
                                        ),
                                        drc.NamedSlider(
                                            name="Number of cities to explore",
                                            id="slider-dataset-sample-size",
                                            min=10,
                                            max=500,
                                            step=10,
                                            marks={
                                                str(i): str(i)
                                                for i in range(10, 501, 100)
                                            },
                                            value=10,
                                        ),
                                    ]
                                ),
                            ],
                        ),
                        dcc.Loading(
                            children=[
                                html.Div(
                                    id="svm-graph-container",
                                    children=dcc.Loading(
                                        className="graph-wrapper",
                                        children=dcc.Graph(
                                            id="graph-tsp"),
                                        style={"display": "none"},
                                    ),
                                ),
                            ]
                        ),
                    ],
                )
            ],
        ),
        html.Img(src=app.get_asset_url(
            "resultats/figures/fig_distances.svg")),
        html.Img(src=app.get_asset_url(
            "resultats/figures/fig_temps_calcul.svg"))
    ]
)


@ app.callback(
    Output("graph-tsp", "figure"),
    Input('slider-dataset-sample-size', 'value'),
    Input('dropdown-select-algorithm', 'value')
)
def update_random_graph(taille_dataset, algo):
    # Initialisation du dataframe
    data = init_random_df(taille_dataset)

    # Initialisation de la matrice des distances relatives
    mat_distance = matrice_distance(data)

    if algo == 0:
        # On prend un chemin initial meilleur qu'un chemin aléatoire
        # Attention cheminInitial est la liste des chemin exploré par l'algorithme
        # plus_proche_voisin
        chemin_initial, temps_calcul = src.algo_proche_voisin.plus_proche_voisin(
            mat_distance)

        # Lancement de l'algorithme 2-opt
        df_res = src.algo_2_opt.main(
            mat_distance, chemin_initial)
    elif algo == 1:
        # Lancement de l'algorithme plus proche voisin
        df_res = src.algo_proche_voisin.main(mat_distance)
    else:
        df_res = src.algo_genetique.main(data, mat_distance)

    # La solution trouvée par l'algo choisi
    solution_figure = affichage(df_res, data)

    return solution_figure


# Running the server
if __name__ == '__main__':
    app.run_server(debug=True)
