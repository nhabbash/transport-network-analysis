import networkx as nx
import clustering as cl

import pprint
import matplotlib.pyplot as plt

pp = pprint.PrettyPrinter(indent = 4)

metro = nx.read_gml("data/graph/metro.gml")
bus = nx.read_gml("data/graph/bus.gml").to_undirected()
tram = nx.read_gml("data/graph/tram.gml").to_undirected()

metro_nodes = list(metro.nodes(data = True))
bus_nodes = list(bus.nodes(data = True))
tram_nodes = list(tram.nodes(data = True))

stops = metro_nodes# + bus_nodes + tram_nodes

regions = cl.cluster_stops(stops, 1)
points = [x["coord"] for _, x in regions.items()]

region_neighbors = cl.get_neighbor_list(points)
neighbor_graph = nx.Graph(region_neighbors)

for n in neighbor_graph:
    neighbor_graph.nodes[n]["coord"] = regions[n]["coord"]

