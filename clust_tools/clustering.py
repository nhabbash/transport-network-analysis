from geopy.distance import distance
from scipy.spatial import Delaunay
from collections import defaultdict
import itertools
import networkx as nx

def add_member(cell, new_member, recompute_centroid = False):
    """
    Adds stop to a cell and recomputes centroid

    Args:
        cell (dict): a cell such as {"coord" : (lon, lat), "members" : [x, y, ...]}
        new_member (tuple): a stop such as ("stop ID", {"stop data"})

    Returns:
        cell (dict): updated cell
    """

    cell["members"].append(new_member[0])

    stop_coord = [float(i) for i in new_member[1]["coord"].split(",")]
    cell["coords"].append(stop_coord)

    if recompute_centroid:
        centroid = [0.0, 0.0]

        for coord in cell["coords"]:
            centroid[0] += coord[0]
            centroid[1] += coord[1]

        centroid = [x / len(cell["coords"]) for x in centroid]
        cell["centroid"] = centroid
    return cell

def find_closest(stop_coord, cells, radius):
    """
    Finds closest cell to a coordinate

    Args:
        stop_coord (list): coordinates of a stop such as (lat, lon)
        cells (dict): a dict of cells such as {id : {"coord" : (lon, lat), "members" : [x, y, ...]}}

    Returns:
        key (int): key of the closest cell to the stop
    """

    closest_cell_key = -1
    min_dist = radius

    # Candidate closest cell for stops that can't find any by the given radius
    min_dist_candidate = 100
    closest_cell_key_candidate = -1
    if cells:
        for key, cell in cells.items():
            cell_centroid = cell["centroid"]
            dist = distance(stop_coord, cell_centroid).km

            if dist <= min_dist_candidate:
                min_dist_candidate = dist
                closest_cell_key_candidate = key

            if dist <= min_dist:
                min_dist = dist
                closest_cell_key = key

    return closest_cell_key, closest_cell_key_candidate
     
def cluster_stops(stops, radius):
    """
    Grouping points into cells with a desired radius

    Args:
        stops (list): List of stops
        radius (float)

    Returns:
        cells (dict): a dict of cells such as {id : {"coord" : (lon, lat), "members" : [x, y, ...]}}
    """

    cells = {}

    # Generate cells
    for stop in stops:
        stop_coord = [float(i) for i in stop[1]["coord"].split(",")]
        key, _ = find_closest(stop_coord, cells, radius)

        if key != -1:
            cells[key] = add_member(cells[key], stop, True)
        else:
            cell = {"centroid" : stop_coord, "members" : [stop[0]], "coords" : [stop_coord]}
            cells[len(cells)] = cell

    # Remove members while keeping centroids
    for _, cell in cells.items():
        cell["centroid_generators"] = cell["members"]
        cell["centroid_coords"] = cell["coords"]
        cell["members"] = []
        cell["coords"] = []

    # Redistribute stops
    stops_mapping = {}
    for stop in stops:
        stop_coord = [float(i) for i in stop[1]["coord"].split(",")]
        key, secondary_key = find_closest(stop_coord, cells, radius)

        if key == -1:
            key = secondary_key

        cells[key] = add_member(cells[key], stop)
        stops_mapping[stop[0]] = key

    return cells, stops_mapping

def get_neighbor_list(points, radius = 5):
    """
    Generates neighbor list for each node through the Delaunay triangulation

    Args:
        points (list): List of coordinates
        radius (float): Maximum distance between neighbors

    Returns:
        neighbors (dict): a dict of neighbors indices (based on points indices)
    """

    tri = Delaunay(points)
    neighbors = defaultdict(set)
    
    for p in tri.vertices:        
        for i, j in itertools.combinations(p, 2):
            i = i.item()
            j = j.item()
            dist = distance(points[i], points[j]).km
            if dist <= radius:
                neighbors[i].add(j)
                neighbors[j].add(i)

    return neighbors

def c2c_flow_graph(net, stops_mapping):
    """
    Generates a region graph with cell-to-cell flow between the subnodes in the regions

    Args:
        net (networkx graph): Complete network containing all the edges
        stops_mapping (dict): Mapping of stops and their corrispective region

    Returns:
        c2c_graph (networkx graph)
    """

    g = nx.Graph()
    g.add_nodes_from(list(set(stops_mapping.values())))
    
    for stop, cur_region in stops_mapping.items():
        edges = net.edges(stop)
        for edge in edges:
            dest_region = stops_mapping[edge[1]]
            if dest_region != cur_region:
                if g.has_edge(cur_region, dest_region):
                    g[cur_region][dest_region]["weight"] += 1
                else:
                    g.add_edge(cur_region, dest_region, weight = 1)
    return g