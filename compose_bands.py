#---------------------------------------------------------------------------------------
# Script author:    Nathalia De Oliveira Silva
# Versions:         ArcGIS 10.2; Python 2.7.5
# Purpose:          The script uses a for loop to go through a group of Landsat images
#                   and creates false color compositions for each one, then saves them
#                   as .jp2 files.
# --------------------------------------------------------------------------------------

import arcpy, os

#Insert in the workspace variable the path to a folder containing the folders to each image
arcpy.env.workspace = r''
#Output path
outws = r''

#Create a list with all the folders inside the workspace
folders = arcpy.ListWorkspaces()

#Create an empty array to store the bands o interest
newrasters_l8 = []

#For loop to compose the bands
for folder in folders:
    #Split the folder's name from the letter P, the folders used here are the folders created from the extraction of LANDSAT8, sensor OLI images
    name = folder.split('P')
    #The part I'm most intereted is the second part of the variable name, the one with date and orbit information
    basename = name[1]
    #Set the worksapce to the current folder 
    arcpy.env.workspace = folder
    #List all the TIFF files with names starting with LC08
    rasters = arcpy.ListRasters("LC08*", "TIF")
    #Check if there are 12 files in the folder
    if len(rasters) == 12:
        #Choose the bands you insterested in, in this case 3,4,5 and 6
        newrasters_l8.append(rasters[3])
        newrasters_l8.append(rasters[4])
        newrasters_l8.append(rasters[5])
        newrasters_l8.append(rasters[6])
        #Set the output information (orbit and date) and the extention as well
        out_raster = os.path.join(outws, "o" + basename[1:8] + basename[10:16] + ".jp2")
        #Compose bands
        arcpy.CompositeBands_management(newrasters_l8, out_raster)
        #Clean the list to the next folder
        newrasters_l8 = []
