import matplotlib.pyplot as plt

def plot_solution(data, manager, routing, solution):
    import datetime

    # Get today's date
    today = datetime.datetime.today()

    # Format today's date as a string in the format YYYY-MM-DD
    today_str = today.strftime('%Y-%m-%d %H:%M:%S')
    
    """Plots the solution on a graph."""
    # First, we need to extract the coordinates from the time_matrix as the time_matrix does not directly provide coordinates.
    # For simplicity, let's create a list of coordinates, assuming that the time_matrix is symmetric and represents a grid-like distance.
    # This is an example and you should replace it with your actual coordinates.
    coordinates = [(i % 3, i // 3) for i in range(len(data['time_matrix']))]

    # Create a scatter plot for the locations
    for i, coord in enumerate(coordinates):
        plt.scatter(coord[0], coord[1], c='blue' if i in data['starts'] else 'red')
        # Annotate the index for each point
        plt.annotate(str(i), (coord[0], coord[1]))

    # Plotting each vehicle's route
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        while not routing.IsEnd(index):
            previous_index = manager.IndexToNode(index)
            index = solution.Value(routing.NextVar(index))
            current_index = manager.IndexToNode(index)
            plt.plot([coordinates[previous_index][0], coordinates[current_index][0]],
                     [coordinates[previous_index][1], coordinates[current_index][1]], 'k')

    # Show the plot
    plt.title('Vehicle Routing Plot')
    plt.savefig('route_{}.png'.format(today_str))
    plt.show()