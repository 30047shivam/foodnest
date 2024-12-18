import pandas as pd
from pulp import LpProblem, LpVariable, LpMinimize, lpSum, PULP_CBC_CMD

def optimize_rider_assignment(data_path, rider_capacity=20):
    """Assigns riders to orders while respecting their capacity."""
    # Load data
    data = pd.read_csv(data_path)

    # Orders and riders
    orders = data["OrderID"].tolist()
    num_riders = -(-len(orders) // rider_capacity)  # Calculate the number of riders, rounding up

    # Decision Variables
    assignment = LpVariable.dicts("Assign", [(i, j) for i in range(num_riders) for j in orders], cat="Binary")

    # Define problem
    prob = LpProblem("RiderAssignment", LpMinimize)

    # Objective: Dummy objective (0) for now as no real metric is given
    prob += 0, "DummyObjective"

    # Constraints: Each order must be assigned to exactly one rider
    for j in orders:
        prob += lpSum(assignment[(i, j)] for i in range(num_riders)) == 1, f"Order_{j}_Assignment"

    # Constraints: Each rider can handle at most 'rider_capacity' orders
    for i in range(num_riders):
        prob += lpSum(assignment[(i, j)] for j in orders) <= rider_capacity, f"Rider_{i}_Capacity"

    # Solve the problem
    prob.solve(PULP_CBC_CMD(msg=False))

    # Output results
    result = {}
    for i in range(num_riders):
        assigned_orders = [j for j in orders if assignment[(i, j)].varValue == 1]
        if assigned_orders:  # Only include riders with assigned orders
            result[f"Rider {i+1}"] = assigned_orders

    return result

if __name__ == "__main__":
    data_path = "data/synthetic_data.csv"
    results = optimize_rider_assignment(data_path, rider_capacity=20)

    # Display results
    for rider, orders in results.items():
        print(f"{rider}: {orders}")
