from geopy.distance import vincenty
import pprint

def add_member(cell, new_member, recompute_centroid = False):
    """
    Adds stop to a cell and recomputes centroid

    Args:
        cell (dict): a cell such as {"coord" : (lon, lat), "members" : [x, y, ...]}
        new_member (tuple): a stop such as ("stop ID", {"stop data"})

    Returns:
        cell (dict): updated cell
    """

    cell["members"].append(new_member)

    if recompute_centroid:
        centroid = [0, 0]
        for stop in cell["members"]:
            stop_coord = [float(i) for i in stop[1]["coord"].split(",")]
            centroid[0] += stop_coord[0]
            centroid[1] += stop_coord[1]

        centroid = [x / len(cell["members"]) for x in centroid]
        cell["coord"] = centroid
    
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
    if cells:
        for key, cell in cells.items():
            cell_coord = cell["coord"]
            # Vincenty distance between two coordinates
            dist = vincenty(stop_coord, cell_coord).km
            if dist <= radius:
                closest_cell_key = key

    return closest_cell_key

        
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
        key = find_closest(stop_coord, cells, radius)

        if key != -1:
            key = find_closest(stop_coord, cells, radius)
            cells[key] = add_member(cells[key], stop, True)
        else:
            cell = {"coord" : stop_coord, "members" : [stop]}
            cells[len(cells)] = cell  

    # Remove members while keeping centroids
    for key, cell in cells.items():
        cell["members"] = []

    # Redistribute stops
    for stop in stops:
        stop_coord = [float(i) for i in stop[1]["coord"].split(",")]
        key = find_closest(stop_coord, cells, radius)
        cells[key] = add_member(cells[key], stop)
    
    return cells