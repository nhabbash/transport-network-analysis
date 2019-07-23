# Transportation Network Analysis
> Analysis of Milan's public transportation network through a multi-layered graph representing different entities

Final project for the *Data Analytics* course for the MSc in Computer Science at University of Milano-Bicocca.

## Brief

The project aimed to analyze the structure of the city network using multilayer graph representing the union of the different available means of transportation.

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
