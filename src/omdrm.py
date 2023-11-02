from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data_model():
    """Stores the data for the problem."""
    data = {}
    # Each row now represents a depot or location, and each column represents the time to travel to another depot or location.
    # We're using a 9x9 matrix for 5 depots and 4 locations.
    data['time_matrix'] = [
        [0, 6, 9, 5, 8, 10, 7, 9, 8],  # Depot 0 to others
        [6, 0, 7, 3, 2, 6, 7, 5, 8],   # Location 1 to others
        [9, 7, 0, 4, 8, 9, 8, 10, 7],  # Location 2 to others
        [5, 3, 4, 0, 3, 8, 9, 4, 3],   # Location 3 to others
        [8, 2, 8, 3, 0, 5, 6, 2, 3],   # Location 4 to others
        [10, 6, 9, 8, 5, 0, 4, 6, 5],  # Depot 1 to others
        [7, 7, 8, 9, 6, 4, 0, 5, 8],   # Depot 2 to others
        [9, 5, 10, 4, 2, 6, 5, 0, 3],  # Depot 3 to others
        [8, 8, 7, 3, 3, 5, 8, 3, 0],   # Depot 4 to others
    ]

    data['time_windows'] = [
        (0, 50),  # Depot 0
        (0, 50),  # Location 1
        (0, 50),  # Location 2
        (0, 50),  # Location 3
        (0, 50),  # Location 4
        (0, 50),  # Depot 1
        (0, 50),  # Depot 2
        (0, 50),  # Depot 3
        (0, 50),  # Depot 4
    ]

    data['num_vehicles'] = 4
    # Depots where each vehicle starts and ends
    data['starts'] = [0, 5, 7, 8]  # Starting depot index for vehicles 0 to 3
    data['ends'] = [0, 5, 7, 8]    # Ending depot index for vehicles 0 to 3
    return data

def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    time_dimension = routing.GetDimensionOrDie('Time')
    total_time = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = f'Route for vehicle {vehicle_id}:\n'
        route_time = 0
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            plan_output += f'{manager.IndexToNode(index)} Time({solution.Min(time_var)}, {solution.Max(time_var)}) -> '
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_time += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        time_var = time_dimension.CumulVar(index)
        plan_output += f'{manager.IndexToNode(index)} Time({solution.Min(time_var)}, {solution.Max(time_var)})\n'
        plan_output += f'Time of the route: {route_time}min\n'
        print(plan_output)
        total_time += route_time
    print(f'Total time of all routes: {total_time}min')

def main():
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['time_matrix']),
                                           data['num_vehicles'], 
                                           data['starts'], 
                                           data['ends'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def time_callback(from_index, to_index):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['time_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(time_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Time Windows constraint.
    time = 'Time'
    routing.AddDimension(
        transit_callback_index,
        30,  # allow waiting time
        50,  # maximum time per vehicle
        False,  # Don't force start cumul at zero.
        time)
    time_dimension = routing.GetDimensionOrDie(time)
    # Add time window constraints for each location except depots.
    for location_idx, time_window in enumerate(data['time_windows']):
        if location_idx in data['starts']:
            continue  # Skip depots
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
    else:
        print("No solution found!")

if __name__ == '__main__':
    main()
