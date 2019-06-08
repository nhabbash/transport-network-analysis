import networkx as nx
import clustering as cl
import pprint

metro = nx.read_gml("data/graph/metro.gml")
bus = nx.read_gml("data/graph/bus.gml").to_undirected()
tram = nx.read_gml("data/graph/tram.gml").to_undirected()

metro_nodes = list(metro.nodes(data = True))
bus_nodes = list(bus.nodes(data = True))
tram_nodes = list(tram.nodes(data = True))

# All the stops in the three networks as a list of tuples such as:
# ("stop ID", {"stop data"})
stops = metro_nodes# + bus_nodes + tram_nodes

cells = cl.cluster_stops(stops, 1)

pp = pprint.PrettyPrinter(indent = 4)
pp.pprint(cells)
exit()