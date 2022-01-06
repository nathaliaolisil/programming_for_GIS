#-----------------------------------------------------------------------
# Script author:    Nathalia De La Fuente Oliveira
# Versions:         ArcGIS 10.2; Python 2.7.5
# Purpose:          The script does:
#                   - Add a new field to the dataset
#                   - Add a new row to the dataset
#                   - Update the attribute table
#                   - Perform a calculation in the new field 
# ----------------------------------------------------------------------

import arcpy
import os

# Set workspace environment: database
arcpy.env.workspace = r"C:\"
wksp = arcpy.env.workspace

# Assign variable
airports = "Airports_pts_Class10_cursors"
print ("airports exists: {}\n".format(arcpy.Exists(airports)))

# Create a new field of your choice in the airports dataset using the ArcPy AddField function (arcpy.AddField())
print ("Adding new field to airports...\n")
arcpy.AddField_management(airports, "USE_ID", "TEXT")

# Print list of fields in airports to check if the new field exists
for field in arcpy.ListFields(airports):
    print (field.name)

# Calculate the new field values using an update cursor
print ("\n Calculating new values for USE_ID...")
with arcpy.da.UpdateCursor(airports, ["USE", "USE_ID"]) as UpdateCursor:
    for row in UpdateCursor:
        if row[0] == "PU":
            row[1] = 1
        if row[0] == "PR":
            row[1] = 2
        
        UpdateCursor.updateRow(row)
    
# Add a new row for a new airport using an insert cursor
print ("Adding new airport to airports...\n")
xy = (-73.947006, 40.7893)
InsertCursor = arcpy.da.InsertCursor(airports, ["SHAPE@XY", "LOC_ID", "NAME", "OWNERNAME", "USE", "USE_ID"])
InsertCursor.insertRow([xy, "NDO", "EHS AIRPORT", "Nathalia De Oliveira", "PR", "2"])
del InsertCursor
    
#Finish script
print ("\n Script finished.")
