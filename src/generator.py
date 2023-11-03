from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data_model_one_vehicle():
    """Stores the data for the problem."""
    data = {}
    # Each row now represents a depot or location, and each column represents the time to travel to another depot or location.
    # We're using a 9x9 matrix for 1 depots and 4 locations.
    data['time_matrix'] = [
        [0, 6, 9, 5, 8, 10, 7, 9, 8],  # Depot 0 to others
        [6, 0, 7, 3, 2, 6, 7, 5, 8],   # Location 1 to others
        [9, 7, 0, 4, 8, 9, 8, 10, 7],  # Location 2 to others
        [5, 3, 4, 0, 3, 8, 9, 4, 3],   # Location 3 to others
        [8, 2, 8, 3, 0, 5, 6, 2, 3],   # Location 4 to others
    ]

    data['time_windows'] = [
        (0, 50),  # Depot 0
        (0, 50),  # Location 1
        (0, 50),  # Location 2
        (0, 50),  # Location 3
        (0, 50),  # Location 4
    ]

    data['num_vehicles'] = 1
    # Depots where each vehicle starts and ends
    data['starts'] = [0]  # Starting depot index for vehicle
    data['ends'] = [0]   # Ending depot index for vehicle
    return data

import random

def create_data_model_f(num_vehicles, num_locations, num_depots):
    """Stores the data for the problem with a variable number of vehicles, locations, and depots."""
    total_nodes = num_locations + num_depots
    data = {}
    # Randomly generate a time_matrix for simplicity in this example
    # In a real scenario, this should be actual distances or times between nodes
    data['time_matrix'] = [[random.randint(1, 10) for _ in range(total_nodes)] for _ in range(total_nodes)]

    # Set diagonal to zero since there's no travel time from a node to itself
    for i in range(total_nodes):
        data['time_matrix'][i][i] = 0

    # Set time windows to be the same for all locations for simplicity
    # In a real scenario, these should be specific time windows for each location
    data['time_windows'] = [(0, 50) for _ in range(total_nodes)]

    data['num_vehicles'] = num_vehicles

    # Assuming all vehicles start and end at the first 'num_depots' nodes
    # In a real scenario, the starting and ending nodes may differ
    data['starts'] = [i for i in range(num_depots)]
    data['ends'] = [i for i in range(num_depots)]

    return data
