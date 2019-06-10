import networkx as nx
import clustering as cl

import pprint
import matplotlib.pyplot as plt

pp = pprint.PrettyPrinter(indent = 4)

metro = nx.read_gml("data/graph/metro.gml")
bus = nx.Graph(nx.read_gml("data/graph/bus.gml").to_undirected())
tram = nx.Graph(nx.read_gml("data/graph/tram.gml").to_undirected())

metro_nodes = list(metro.nodes(data = True))

# Bus and tram share some stops, some processing is needed before uniting the nets. In the composition, bus attributes take the precedence
bus_tram = nx.compose(tram, bus)

for node in tram.nodes(data = True):
    if node[1]["routes"] != bus_tram.node[node[0]]["routes"]:
        bus_tram.node[node[0]]["routes"] += "," + (node[1]["routes"])

net = nx.union(metro, bus_tram)

stops = list(net.nodes(data = True))

regions, stops_mapping = cl.cluster_stops(stops, 1)
points = [x["centroid"] for _, x in regions.items()]

region_neighbors = cl.get_neighbor_list(points, 4.5)
neighbor_graph = nx.Graph(region_neighbors)

for n in neighbor_graph:   
    neighbor_graph.nodes[n]["centroid"] = regions[n]["centroid"]
    neighbor_graph.nodes[n]["stops"] = [member for member in regions[n]["members"]]

c2c_graph = cl.c2c_flow_graph(net, stops_mapping)
