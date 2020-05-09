# Transportation Network Analysis
> Analysis of the structure and resilience of a city's public transport network using an average graph representing its heterogeneous means of transportation.

Live Dash [demo](https://transport-network-analysis.herokuapp.com/) on Heroku.

## Structure

The project is structured in four main parts:
* Database container containing the raw GTFS data
    * The CSV to GML conversion of the data (with some processing)
* The graph processing notebook
* The attacks processing notebook
* A visualization demo

#
## Prerequisites

* Python 3.0 or greater
* Other requisites listed in `requirements.txt`

#
## Installation
```sh
$ git clone https://github.com/Dodicin/transportation-network-analysis
$ cd transportation-network-analysis
$ pip install -r requirements.txt
```
#
## Accessing the container
```sh
$ cd container
# Downloads the dataset
$ python init_data.py
# Launch DB
$ docker-compose up --build
``` 
#
## Accessing notebooks
```sh
$ jupyter-notebook maps.ipynb
``` 
#
## Accessing dash demo
```sh
$ python2 dash/demo.py
``` 

#
## Authors

* **Nassim Habbash** (808292) - [dodicin](https://github.com/dodicin)
* **Ricardo Matamoros** (807450) - [ricardo](https://github.com/ricardoanibalmatamorosaragon)
