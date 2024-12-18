import pandas as pd
import numpy as np
import os  # Import os to handle directory creation

def preprocess_data(data):
    """
    This function will clean the input data and return a processed version.
    (Adjust preprocessing logic as required)

    Parameters:
    data (DataFrame): The input data to preprocess.

    Returns:
    DataFrame: The cleaned data.
    """
    # Example preprocessing: remove rows with missing values
    cleaned_data = data.dropna()  # Modify this logic as needed
    return cleaned_data
def generate_synthetic_data(num_orders=1000):
    """Generates synthetic data for delivery optimization."""
    np.random.seed(42)  # For reproducibility

    # Generate random order details
    order_ids = np.arange(1, num_orders + 1)
    restaurant_latitudes = np.random.uniform(26.50, 27.17, size=num_orders)
    restaurant_longitudes = np.random.uniform(80.50, 81.22, size=num_orders)
    customer_latitudes = np.random.uniform(26.50, 27.17, size=num_orders)
    customer_longitudes = np.random.uniform(80.50, 81.22, size=num_orders)
    order_values = np.random.uniform(100, 500, size=num_orders)
    food_prep_time = np.random.randint(5, 15, size=num_orders)  # in minutes

    # Create a DataFrame
    data = pd.DataFrame({
        "OrderID": order_ids,
        "RestaurantLat": restaurant_latitudes,
        "RestaurantLon": restaurant_longitudes,
        "CustomerLat": customer_latitudes,
        "CustomerLon": customer_longitudes,
        "OrderValue": order_values,
        "FoodPrepTime": food_prep_time
    })

    return data

if __name__ == "__main__":
    # Create the 'data' directory if it does not exist
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

    # Generate data
    synthetic_data = generate_synthetic_data()

    # Save the data to a CSV file
    output_file = os.path.join(output_dir, "synthetic_data.csv")
    synthetic_data.to_csv(output_file, index=False)

    print(f"Synthetic data generated and saved to '{output_file}'")
