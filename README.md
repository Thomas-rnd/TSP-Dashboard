# Travelling Salesman Problem (TSP) Solver

This is an exploration app made using the Dash interactive Python framework developed by [Plotly](https://plot.ly/). The goal was to implement an easy way to test the capacity of an algorithm to resolve the TSP. The indicators used are : the computation time and its capacity to find a better solution than other algorithms.

I used Dash to abstract away all of the technologies and protocols required to build an interactive web-based application. It is a simple and effective way to bind a user interface around a Python code. To learn more check out the [documentation](https://plot.ly/dash).

Try out the [demo app here]

![alt text](images/screenshot.png "Screenshot")

## General informations

This demo lets you test several algorithms to resolve the Travelling Salesman Problem (TSP)

### Algorithm implemented

- 2-opt inversion
- Nearest neighbor search
- Genetic algorithm
- Kohonen Self-Organizing Maps

It includes artificially generated datasets that you can modify by changing the sample size with the slider provided.

The other dropdown let you change the algorithm used to resolve the problem.

## Getting Started

### Running the app locally

First create a virtual environment with conda or venv inside a temp folder, then activate it.

```
cd temp
python3 -m venv venv

# Windows
venv\Scripts\activate
# Or Linux and Mac
source venv/bin/activate
```

Clone the git repo, then install the requirements with pip

```
git clone https://github.com/Thomas-rnd/dash_TSP
cd dash_TSP
pip install -r requirements.txt
```

Run the app

```
python app.py
```

## Built With

- [Dash](https://dash.plot.ly/) - Main server and interactive components
- [Plotly Python](https://plot.ly/python/) - Used to create the interactive plots
