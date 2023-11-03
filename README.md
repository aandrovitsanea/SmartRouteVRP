# VRPOptimizer

Welcome to the VRPOptimizer repository! This is an ongoing project dedicated to tackling the complex and challenging Vehicle Routing Problem (VRP), a staple in the field of logistics and supply chain management. Our aim is to develop an efficient and scalable solution that minimizes the total route cost while respecting various constraints such as delivery time windows, vehicle capacities, and customer requirements.

## Optimized Multi-Depot Routing Model (OMDRM)

The [Optimized Multi-Depot Routing Model (OMDRM)](src/solvers.py) is an advanced algorithmic solution for solving complex logistics and transportation challenges. It leverages Google's OR-Tools to efficiently manage a fleet of vehicles across multiple depots, ensuring timely and cost-effective deliveries.

### Overview of OMDRM

- **Manages a fleet of 4 vehicles.**
- **Handles 5 depots and 4 additional delivery locations.**
- **Incorporates time windows to maintain punctual deliveries.**
- **Allows for flexible vehicle deployment with variable start and end depots.**

OMDRM uses a sophisticated approach to minimize total travel time while adhering to the constraints of delivery windows and depot locations.

### How OMDRM Works

1. Initializes data for the routing problem, including a time matrix and time windows for deliveries.
2. Creates a routing index manager and model to facilitate the optimization process.
3. Registers a callback function to calculate travel times between points accurately.
4. Sets up constraints for travel times and delivery windows within the routing model.
5. Employs the OR-Tools solver to determine the most efficient routes.
6. Provides a detailed output of routes, schedules, and total travel time upon finding an optimal solution.

### Expected Output

OMDRM generates an output detailing:
- The order of locations visited by each vehicle.
- Start and finish times for each route.
- Duration of travel between consecutive locations.
- The aggregated time taken for all routes, providing a benchmark for the solution's efficiency.

This model serves as a robust framework for tackling the complexities inherent in multi-depot vehicle routing scenarios.


## Getting Started
[ ] Add docs
To get started with the VRPOptimizer, please refer to the `docs/` directory, which provides comprehensive guidance on setting up the environment, running the code, and contributing to the project.

## Problem Setup

- **Locations**: 5 depots and 4 additional locations.
- **Vehicles**: A fleet of 4 vehicles, each starting from a different depot.
- **Constraints**:
  - Travel time between locations.
  - Time windows for visiting each location.
  - Maximum route duration for each vehicle.

## Prerequisites

- Python 3.x
- OR-Tools library installed via pip:
  ```bash
  pip install ortools

  ```

## Running the Script

In `ipython3` console:

```ipython3
import sys
sys.path.append('../src')
import solvers as solvers
import importlib
import generator
importlib.reload(solvers)
importlib.reload(generator)

data = generator.create_data_model_one_vehicle()
manager, routing, solution = solvers.omdrm_one_vehicle(data)
```
or run [notebook](notebooks/app_1_vehicle.ipynb).

**Sample ouput**

```bash
Route for vehicle 0:
 0 -> 1 -> 4 -> 3 -> 2 -> 0
Distance of the route: 24m

Maximum of the route distances: 24m

```

<img src="notebooks/route_2023-11-03 10:19:18.png" alt="Optimized route for 1 vehicle">

## Repository Contents

- `src/`: This directory contains all the source code for the VRP algorithms implemented in Python. It includes modules for data preprocessing, optimization algorithms, and post-processing of results.

- `data/`: Sample datasets are stored here. They provide the information necessary to test and evaluate the performance of the VRP algorithms, including distances, demands, time windows, and vehicle capacities.

- `notebooks/`: Jupyter notebooks with detailed examples, visualizations, and step-by-step guides on how to use and modify the VRP algorithms.

- `docs/`: Documentation on the methodology, code usage, and background theory. It includes setup instructions, function descriptions, and a detailed explanation of the problem statement.

- `tests/`: Automated tests to ensure the reliability and stability of the algorithms as the codebase evolves.

- `utils/`: Utility scripts and helper functions that support data manipulation, result analysis, and other common tasks.

- `Dockerfile`: For containerizing the application, making it easy to deploy the VRP solution in any environment.

- `requirements.txt`: A list of Python dependencies required to run the code.

- `LICENSE`: The license file detailing how the code can be used by others.

## Features

- **Custom VRP Solver**: A Python-based solver that uses heuristic and metaheuristic approaches to find near-optimal solutions.

- **Scalable and Modular**: Designed to be adaptable to different types of VRP variations including Capacitated VRP, VRP with Time Windows, and more.

- **Visualization**: Tools to visualize routing solutions on maps for easy analysis and reporting.

- **Extensive Documentation**: Everything you need to understand the problem, use the code, and adapt it to your specific needs.

- **Community-Driven**: Contributions are welcome! Whether it's a new feature, bug fix, or an improvement in the documentation, community input is valued.

- **Multiple Depots**: Supports routing for vehicles originating from different depots.

- **Time Windows**: Each location has a time window within which the delivery or service must be made.

- **Fleet Management**: Optimizes routes for multiple vehicles and ensures that the workload is distributed among the available vehicles.

- **Constraints Handling**: Takes into account travel times and service times, ensuring that each location is visited within its specified time window.

## TODOs

[ ] Fix generalization for multiple vehicles, routes, depos.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. Check out the `CONTRIBUTING.md` file on how to get started.

## License

Distributed under the MIT License. See `LICENSE` for more information.
