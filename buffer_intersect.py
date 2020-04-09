#-------------------------------------------------------------------------------
# Script author:    Nathalia De Oliveira Silva
# Versions:         ArcGIS 10.2; Python 2.7.5
# Purpose:          The script gives as an output a layer with the blocks that 
#                   are half mile from a shapefile of the subway stations in NY.
# ------------------------------------------------------------------------------

import arcpy

# Overwrite existing output
arcpy.env.overwriteOutput = True

# Set workspace: a database
arcpy.env.workspace = r"C:\"
wksp = arcpy.env.workspace

#Assign variables
Subway_Stns = wksp + "\NYC_Subway_Stations"
NYC_2010_CB_Dem = wksp + "\NYC_2010_CensusBlocks"

# Create a half mile buffer of all subway station
print ("Running buffer tool...")
buf_result = arcpy.Buffer_analysis(Subway_Stns, "Subway_buffer", "2640 FEET", "", "", "ALL")

#Intersection between subway stations and census blocks
print ("intersection census blocks...")
arcpy.Intersect_analysis([NYC_2010_CB_Dem, buf_result], "NYC_2010_CB_DEM_IntersectBuffer")




