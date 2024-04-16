import pandas as pd
import folium
import time
from geopy.distance import geodesic

csv_file_path = 'flight_data.csv'
map_file_path = 'map.html'
# Initialize the map at a default location
initial_location = [13.0636, 77.36]  # Adjust this if you have a better initial center
total_distance = 0.0
points = []
map = folium.Map(location=initial_location, zoom_start=12)

def read_csv_to_df(csv_path):
    # Read CSV without headers; names are assigned for convenience
    return pd.read_csv(csv_path, usecols=[9, 10], header=None, names=['latitude', 'longitude'])

def update_map(df, map, last_known_index, total_distance):
    global points  # Make sure to use the global points if it's needed outside the function
    last_point = points[-1] if points else None  # Start with the last point from previous updates

    for index, row in df.iloc[last_known_index:].iterrows():
        current_point = [row['latitude'], row['longitude']]
        folium.CircleMarker(
            location=current_point,
            radius=4,  # Small radius for a dot-like appearance
            color='orange',  # Color of the dot
            fill=True,
            fill_color='red',
            fill_opacity=0.9
        ).add_to(map)
        # Add marker of coordinates
        folium.Marker(
            location=current_point,
            icon=folium.DivIcon(html=f'<div style="color: red; font-size: 12pt">{row["latitude"]}, {row["longitude"]}</div>')
        ).add_to(map)
        points.append(current_point)
        print(f"Added marker for ({row['latitude']}, {row['longitude']}) at {time.ctime()}")
        # Calculate the distance from the last point
        if last_point:
            total_distance += geodesic(last_point, current_point).kilometers
        last_point = current_point

    if points:
        print(points)
        folium.PolyLine(points, color='orange', weight=1.1, opacity=0.8).add_to(map)

    distance_marker_location = [points[-1][0] + 0.005, points[-1][1]]
    folium.Marker(
        location=distance_marker_location,
        icon=folium.DivIcon(html=f'<div style="color: black; font-size: 12pt">{total_distance:.2f} km</div>')
    ).add_to(map)
    
    map.save(map_file_path)
    return total_distance

last_known_index = 0

while True:
    df = read_csv_to_df(csv_file_path)
    current_size = len(df)

    if current_size > last_known_index:
        total_distance = update_map(df, map, last_known_index, total_distance)  # Update global total_distance
        last_known_index = current_size

    time.sleep(5)  # check the file every 5 seconds
