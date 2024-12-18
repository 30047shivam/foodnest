import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

class OSRMRouteOptimizer:
    """
    A class to interact with the OSRM API for route optimization.
    """

    BASE_URL = "http://router.project-osrm.org/route/v1/driving/"

    @staticmethod
    def fetch_route(coordinates, overview="false", steps="false"):
        """
        Fetch route details from OSRM API.

        Parameters:
        - coordinates (list of tuples): List of waypoints (latitude, longitude).
        - overview (str): Include geometry overview ('false', 'simplified', 'full').
        - steps (str): Include turn-by-turn instructions ('true' or 'false').

        Returns:
        - dict: Parsed OSRM response containing duration, distance, and optional route details.
        """
        try:
            # Validate coordinates format
            if not all(len(coord) == 2 for coord in coordinates):
                raise ValueError("Coordinates must be a list of tuples with exactly 2 values (latitude, longitude).")

            # Build query string
            formatted_coords = ";".join([f"{lon},{lat}" for lat, lon in coordinates])
            query = f"{formatted_coords}?overview={overview}&steps={steps}"

            logging.info(f"Fetching route for coordinates: {coordinates}")
            logging.info(f"Formatted query string: {query}")

            # Make API request
            response = requests.get(OSRMRouteOptimizer.BASE_URL + query)
            response.raise_for_status()

            # Parse response
            data = response.json()
            logging.info(f"Raw OSRM response: {data}")

            if 'routes' not in data or not data['routes']:
                raise ValueError("No routes found in response.")

            route = data['routes'][0]  # Extract the first route
            logging.info(f"Processing first route: {route}")

            # Validate route structure
            duration = route.get("duration")
            distance = route.get("distance")
            legs = route.get("legs", [])

            if duration is None or distance is None:
                raise ValueError("Missing necessary fields (duration or distance) in route response.")

            # Safely process legs and steps
            processed_legs = []
            for leg_index, leg in enumerate(legs):
                logging.info(f"Leg {leg_index + 1}: {leg}")
                steps = leg.get("steps", [])
                for step_index, step in enumerate(steps):
                    maneuver = step.get("maneuver", {}).get("instruction", "No instruction available")
                    logging.info(f"Step {step_index + 1}: {maneuver}")
                processed_legs.append({"steps": steps})

            return {
                "duration": duration,  # in seconds
                "distance": distance,  # in meters
                "legs": processed_legs,  # Processed legs and steps
            }

        except requests.RequestException as e:
            logging.error(f"Error: Failed to fetch route data. {e}")
            return None
        except (KeyError, ValueError) as e:
            logging.error(f"Error: Invalid response structure. {e}")
            return None

    @staticmethod
    def format_duration(duration_seconds):
        """
        Format duration from seconds to hours, minutes, and seconds.

        Parameters:
        - duration_seconds (float): Duration in seconds.

        Returns:
        - str: Formatted duration.
        """
        hours, rem = divmod(int(duration_seconds), 3600)
        minutes, seconds = divmod(rem, 60)
        return f"{hours}h {minutes}m {seconds}s"

    @staticmethod
    def optimize_route(coordinates):
        """
        Optimize a route based on a list of coordinates (waypoints).

        Parameters:
        - coordinates (list of tuples): List of waypoints (latitude, longitude).

        Returns:
        - dict: Optimized route details, including duration, distance, and steps.
        """
        logging.info(f"Optimizing route for coordinates: {coordinates}")

        # Fetch route data
        route_data = OSRMRouteOptimizer.fetch_route(coordinates)

        if route_data:
            formatted_duration = OSRMRouteOptimizer.format_duration(route_data["duration"])
            logging.info(f"Optimized Route Duration: {formatted_duration}")
            logging.info(f"Optimized Route Distance: {route_data['distance']:.2f} meters")
            return route_data
        else:
            logging.error("Failed to optimize route.")
            return None


if __name__ == "__main__":
    # Example usage
    waypoints = [
        (26.85, 80.95),  # Start latitude and longitude
        (26.88, 81.00),  # Intermediate waypoint
        (26.90, 81.05)   # End latitude and longitude
    ]

    # Fetch and optimize route
    logging.info("Optimizing route...")
    optimized_route = OSRMRouteOptimizer.optimize_route(waypoints)

    # Display optimized route details
    if optimized_route:
        logging.info("Optimized Route Details:")
        logging.info(f"Duration: {optimized_route['duration']} seconds")
        logging.info(f"Distance: {optimized_route['distance']} meters")
        if optimized_route['legs']:
            logging.info("Turn-by-turn Steps:")
            for leg in optimized_route['legs']:
                for step in leg["steps"]:
                    instruction = step.get("maneuver", {}).get("instruction", "No instruction available")
                    logging.info(f"- {instruction}")
    else:
        logging.error("Failed to optimize route.")
