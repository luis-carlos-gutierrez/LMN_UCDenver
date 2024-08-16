import geopy.distance

def has_arrived(target_location, current_location, radius=10):
    """
    Check if the user has arrived at the target location.
    
    Parameters:
    target_location (tuple): (latitude, longitude) of the target location.
    current_location (tuple): (latitude, longitude) of the current location.
    radius (float): Radius in meters within which arrival is considered.
    
    Returns:
    bool: True if the user has arrived, False otherwise.
    """
    distance = geopy.distance.geodesic(target_location, current_location).meters
    return distance <= radius

# Example usage
target_location = (40.748817, -73.985428)  # Example: Latitude and Longitude of Times Square, NYC
current_location = (40.748900, -73.985500)  # Example: Current GPS coordinates

if has_arrived(target_location, current_location, radius=15):
    print("User has arrived at the target location.")
else:
    print("User has not arrived at the target location.")
