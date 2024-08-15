import gpsd
import requests
import polyline
import folium
import subprocess

# Connect to the local gpsd service
gpsd.connect()

# Get the current GPS data
packet = gpsd.get_current()  # Returns GpsResponse class to packet
current_position = packet.position()  # Uses .position() function of GpsResponse Object to get the position of the class.

# Define your API key and endpoint
API_KEY = ''
endpoint = 'https://maps.googleapis.com/maps/api/directions/json'

# Define the parameters
origin = f"{current_position[0]},{current_position[1]}"  # Use the current GPS position as the origin

destination = 'Larimer Square' #Set the destination here
params = {
    'origin': origin,
    'destination': destination,
    'mode': 'walking',  # Specify the mode as walking
    'key': API_KEY
}

# Make a request to the API
response = requests.get(endpoint, params=params)
directions = response.json()

# Extract and decode the overview polyline to get GPS coordinates
if directions['status'] == 'OK':
    overview_polyline = directions['routes'][0]['overview_polyline']['points']
    path_coordinates = polyline.decode(overview_polyline)
    
    print("GPS Coordinates of the walking route:")
    for coord in path_coordinates:
        print(f"Lat: {coord[0]}, Lng: {coord[1]}")

    # Get the start and end locations from the response
    start_location = directions['routes'][0]['legs'][0]['start_location']
    end_location = directions['routes'][0]['legs'][0]['end_location']
    
    # Create a folium map centered at the midpoint between origin and destination
    midpoint = ((start_location['lat'] + end_location['lat']) / 2, (start_location['lng'] + end_location['lng']) / 2)
    folium_map = folium.Map(location=midpoint, zoom_start=14)
    
    # Add markers for origin and destination
    folium.Marker(location=(start_location['lat'], start_location['lng']), popup='Origin: CU Denver North Classroom Building', icon=folium.Icon(color='green')).add_to(folium_map)
    folium.Marker(location=(end_location['lat'], end_location['lng']), popup='Destination: Larimer Square', icon=folium.Icon(color='red')).add_to(folium_map)
    
    # Add the directions to the map
    folium.PolyLine(locations=path_coordinates, color='blue', weight=5, opacity=0.7).add_to(folium_map)
    
    # Add markers for each GPS coordinate with popups
    for coord in path_coordinates:
        popup_text = f"Lat: {coord[0]}, Lng: {coord[1]}"
        folium.Marker(location=(coord[0], coord[1]), popup=popup_text, icon=folium.Icon(color='blue', icon='info-sign')).add_to(folium_map)
    
    # Save the map to an HTML file
    html_file = 'map_with_directions.html'
    folium_map.save(html_file)
    
    # Open the HTML file in Firefox using subprocess
    subprocess.Popen(['firefox', html_file])
else:
    print("Error:", directions['status'])
