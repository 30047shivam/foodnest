import matplotlib.pyplot as plt

def plot_routes(optimized_routes, title="Optimized Delivery Routes"):
    """
    Plot optimized routes on a 2D graph.

    Parameters:
    - optimized_routes (list of dicts): Each dict contains:
        - 'x': List of longitude values (or x-coordinates).
        - 'y': List of latitude values (or y-coordinates).
        - 'route_name': Name of the route for labeling.
        - 'color' (optional): Line color.
        - 'marker' (optional): Marker style.
    - title (str): Title of the plot.
    """
    if not optimized_routes:
        print("Error: No route data provided to plot.")
        return

    plt.figure(figsize=(10, 6))

    for route in optimized_routes:
        x = route.get('x', [])
        y = route.get('y', [])
        route_name = route.get('route_name', "Unnamed Route")
        color = route.get('color', None)
        marker = route.get('marker', None)

        if not x or not y:
            print(f"Warning: Route '{route_name}' has no coordinates to plot.")
            continue

        plt.plot(x, y, label=route_name, color=color, marker=marker, linewidth=2)

    plt.title(title)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_q_values(q_values, title="Q-Values Over Time", labels=None):
    """
    Plot Q-values over episodes.

    Parameters:
    - q_values (list or list of lists): Q-values over episodes.
        - Single list for one series.
        - List of lists for multiple series.
    - title (str): Title of the plot.
    - labels (list): Labels for multiple Q-value series.
    """
    if not q_values:
        print("Error: No Q-values provided to plot.")
        return

    plt.figure(figsize=(10, 6))

    # Support multiple Q-value series
    if isinstance(q_values[0], (list, tuple)):
        for i, series in enumerate(q_values):
            label = labels[i] if labels and i < len(labels) else f"Series {i+1}"
            plt.plot(series, label=label, linewidth=2)
    else:
        plt.plot(q_values, label="Q-Value", linewidth=2)

    plt.title(title)
    plt.xlabel("Episodes")
    plt.ylabel("Q-Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# Example usage
if __name__ == "__main__":
    # Example route data
    optimized_routes = [
        {'x': [80.95, 80.97, 81.00], 'y': [26.85, 26.87, 26.88], 'route_name': "Route 1", 'color': 'blue'},
        {'x': [80.95, 80.96, 80.99], 'y': [26.85, 26.86, 26.89], 'route_name': "Route 2", 'color': 'green', 'marker': 'o'}
    ]

    print("Plotting delivery routes...")
    plot_routes(optimized_routes)

    # Example Q-values data
    q_values = [i**0.5 for i in range(1, 101)]  # Dummy Q-values for one series
    multiple_q_values = [
        [i**0.5 for i in range(1, 101)],       # Series 1
        [i**0.6 for i in range(1, 101)]        # Series 2
    ]
    print("Plotting Q-values...")
    plot_q_values(q_values)
    print("Plotting multiple Q-values...")
    plot_q_values(multiple_q_values, labels=["Series 1 (sqrt)", "Series 2 (pow 0.6)"])
