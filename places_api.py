import requests

# Replace with your actual API key
api_key = ''

# Your GPS coordinates
latitude = 39.7452733
longitude = -105.0017627

# Construct the API request URL
url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=500&key={api_key}"

# Make the API request
response = requests.get(url)

# Check for successful response
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Check if there are results
    if 'results' in data:
        # Print information about each place
        for place in data['results']:
            name = place.get('name', 'Unknown')
            address = place.get('vicinity', 'Unknown')
            location = place.get('geometry', {}).get('location', {})
            lat = location.get('lat', 'Unknown')
            lng = location.get('lng', 'Unknown')
            print(f"Name: {name}\nAddress: {address}\nLatitude: {lat}\nLongitude: {lng}\n")
    else:
        print("No places found.")
else:
    print(f"Error fetching data: {response.status_code}")
