# Transportation Network Analysis
> Analysis of Milan's public transportation network through a multi-layered graph representing different entities

Final project for the *Data Analytics* course for the MSc in Computer Science at University of Milano-Bicocca.

## Brief

The project aimed to analyze the structure of the city network using multilayer graph representing the union of the different available means of transportation.

#
## Prerequisites

* Python 3.0 or greater

### To access the DB with unprocessed GTFS data
* Docker
* Docker Compose
* PostgreSQL (Binary necessary for the psycopg2 Python connector)
* psycopg2

### To generate graphs
* networkx
* geopy
* scipy

### For visualization
* folium
* Jupyter Notebook

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
## Visualizing data
```sh
$ jupyter-notebook maps.ipynb
``` 


#
## Authors

* **Nassim Habbash** (808292) - [dodicin](https://github.com/dodicin)
* **Ricardo Matamoros** (807450) - [ricardo](https://github.com/ricardoanibalmatamorosaragon)
