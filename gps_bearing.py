import math

def calculate_bearing(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    
    # Calculate the difference in longitude
    delta_lon = lon2 - lon1
    
    # Calculate the components of the bearing
    x = math.sin(delta_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon))
    
    # Calculate the initial bearing
    initial_bearing = math.atan2(x, y)
    
    # Convert the initial bearing from radians to degrees
    initial_bearing = math.degrees(initial_bearing)
    
    # Normalize the bearing to 0 - 360 degrees
    compass_bearing = (initial_bearing + 360) % 360
    
    return compass_bearing

# Example usage
lat2 = 39.7517936
lon2 = -104.9026302
lat1 = 39.7523395
lon1 = -104.9018101
bearing = calculate_bearing(lat1, lon1, lat2, lon2)
print("The bearing from point 1 to point 2 is:", bearing)
