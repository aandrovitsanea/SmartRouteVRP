
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import visuals

def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    max_route_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} ->'.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        plan_output += ' {}\n'.format(manager.IndexToNode(index))
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    print('Maximum of the route distances: {}m'.format(max_route_distance))

    
def omdrm_one_vehicle(data):
    print("Create the routing index manager")
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['time_matrix']),
                                           data['num_vehicles'], 
                                           data['starts'], 
                                           data['ends'])
    print("Create Routing Model")
    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    print("Create and register a transit callback")
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
    print("Print solution")
    print_solution(data, manager, routing, solution)
    
    # Print solution.
    if solution:
        visuals.plot_solution(data, manager, routing, solution)
    else:
        print("No solution found!")
        
    return manager, routing, solution

def omdrm_up(data):
    print("Create the routing index manager")
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['time_matrix']),
                                           data['num_vehicles'], 
                                           data['starts'], 
                                           data['ends'])
    print("Create Routing Model")
    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    print("Create and register a transit callback")
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

    # Setting first solution heuristic to PARALLEL_CHEAPEST_INSERTION.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION)

    # Setting the search parameters to use a metaheuristic for better solutions.
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = 30  # Adjust the time limit as needed

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
    print("Print solution")
    print_solution(data, manager, routing, solution)
    
    # Print solution.
    if solution:
        visuals.plot_solution(data, manager, routing, solution)
    else:
        print("No solution found!")
        
    return manager, routing, solution