#---------------------------------------------------------------------------------------
# Script author:    Nathalia De Oliveira Silva
# Versions:         ArcGIS 10.2; Python 2.7.5
# Purpose:          The script uses a for loop to go through a group Landsat images
#                   and creates a false color compositions for each one, then saves them
#                   as .jp2 files.
# --------------------------------------------------------------------------------------

import arcpy
import os

#Insert in the workspace variable the path do a folder containing the folder to each image
arcpy.env.workspace = r'C:\'
#Output path
outws = r''

#Create a list with all the folder inside the workspace
folders = arcpy.ListWorkspaces()
newrasters_l8 = []

#For loop to compose the bands
for folder in folders:
    #Set the worksapce to the current folder 
    arcpy.env.workspace = folder
    #List all the TIF files with names starting with LC08
    rasters = arcpy.ListRasters("LC08*", "TIF")
    #Check if there are 12 files in the folder
    if len(rasters) == 12:
        #Choose the bands you insterested in
        newrasters_l8.append(rasters[3])
        newrasters_l8.append(rasters[4])
        newrasters_l8.append(rasters[5])
        newrasters_l8.append(rasters[6])
        name = str(folder)
        #Set the output information and extention
        out_raster = outws + "\\" + "o" + name[28:35] + name[37:43] + ".jp2"
        print(out_raster)
        #Compose bands
        arcpy.CompositeBands_management(newrasters_l8, out_raster)
        newrasters_l8 = []
