#----------------------------------------------------------------------------
# Script author:    Nathalia De La Fuente Oliveira
# Versions:         ArcGIS 10.2; Python 2.7.5
# Purpose:          The script opens an text file containing addresses 
#                   transforming them into XY coordinates using Google Maps
#                   and saves the output in a new text file .
# ---------------------------------------------------------------------------

#Using Google Maps API

#Open the file containing Addresses
address = open("address.txt")

#Using a for loop to go over the lines with the addresses and geolocate them
for line in endereco:

    from geopy.geocoders import GoogleV3

    #Insert in this variable the API Key 
    api_key = ''

    geolocator = GoogleV3(api_key)

    location = geolocator.geocode(str(line), timeout=100)

    #If it finds a valid location it saves the address and the coordinates in a text file
    if location:
        lat=location.latitude
        longi=location.longitude
        coordinates = open("coordinates.txt", "a")
        coordinates.write("Address: " + line + " ") 
        coordinates.write("Coordinates: " + str((location.latitude, location.longitude)) + "\n")
        coordinates.close()

    #If it doesn's find a valid location it saves the address and sets the coordinates as not found    
    else:
        lat = None
        lon = None
        coordinates = open("coordinates.txt", "a")
        coordinates.write("Address: " + line + " ") 
        coordinates.write("Coordinates: Not found")
        coordinates.close()

        

