# Transportation Network Analysis
> Graph-based analysis of Milan's public transportation network

<p align="center">
  <img  src="docs/images/net-voronoi.png" width="55%">
  <br>
  <em>Voronoi diagram of the neighbor graph with γ=2km and ρ=5km</em>
</p>

## Overview
This work is a graph-based analysis of a city's public transport network. It uses an average, aggregated graph to represent the different means of public transportation offered by the city, inspecting its structure, connectivity and resilience to different failure/attack strategies. 
More information on the technical aspects of the work can be found in the report and project presentation under [`docs`](/docs).

Live Dash [demo](https://transport-network-analysis.herokuapp.com/) on Heroku.

#
## Prerequisites

* Python 3.0 or greater for the clustering tools and notebooks
* Python 2.7 for the demo

#
## Installation
```sh
$ git clone https://github.com/Dodicin/transportation-network-analysis
$ cd transportation-network-analysis
$ pip install -r requirements.txt
```

## Structure
The project is structured in four main components:
* Database container containing the raw GTFS data
    * The CSV to GML conversion of the data (with some processing)
* The graph processing notebook
* The attacks processing notebook
* A visualization demo

#
### Accessing the container
```sh
$ cd container
# Downloads the dataset
$ python init_data.py
# Launch DB
$ docker-compose up --build
``` 

### Accessing notebooks
```sh
$ jupyter-notebook maps.ipynb
``` 

### Accessing dash demo locally
```sh
$ python2 dash/demo.py
``` 

#
## Authors

* **Nassim Habbash** (808292) - [nhabbash](https://github.com/nhabbash)
* **Ricardo Matamoros** (807450) - [ricardo](https://github.com/ricardoanibalmatamorosaragon)
