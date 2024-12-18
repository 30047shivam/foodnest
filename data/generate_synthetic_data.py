import pandas as pd
import random

# Set the number of records to generate
num_records = 100

# Function to generate random coordinates
def random_coordinates():
    # Generate latitude and longitude within a reasonable range
    latitude = round(random.uniform(20.0, 50.0), 6)  # Random latitude
    longitude = round(random.uniform(-125.0, -65.0), 6)  # Random longitude
    return latitude, longitude

# Generate synthetic data
data = []
for i in range(1, num_records + 1):
    source_lat, source_lon = random_coordinates()
    dest_lat, dest_lon = random_coordinates()
    delivery_time = random.randint(30, 180)  # Random delivery time in minutes
    vehicle_capacity = random.choice([10, 20, 30, 40, 50])  # Random vehicle capacity
    
    data.append([
        f"order_{i}", source_lat, source_lon, dest_lat, dest_lon, delivery_time, vehicle_capacity
    ])

# Create a DataFrame
columns = [
    "order_id", "source_latitude", "source_longitude",
    "destination_latitude", "destination_longitude",
    "delivery_time", "vehicle_capacity"
]
df = pd.DataFrame(data, columns=columns)

# Save the DataFrame to a CSV file
output_path = "data/synthetic_data.csv"
df.to_csv(output_path, index=False)

print(f"Synthetic data generated and saved to {output_path}")
