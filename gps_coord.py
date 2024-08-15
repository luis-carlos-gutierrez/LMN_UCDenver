import gpsd

# Connect to the local gpsd service
gpsd.connect()

# Get the current GPS data
packet = gpsd.get_current() # Returns GpsReponse class to packet
print(packet.position()) # Uses .position() function of GpsResponse Object to get the position of the class.
