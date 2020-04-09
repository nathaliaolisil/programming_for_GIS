#---------------------------------------------------------------------------------------
# Script author:    Nathalia De Oliveira Silva
# Versions:         ArcGIS 10.2; Python 2.7.5
# Purpose:          The script uses a for loop to convert a group of raster files to
#                   to point and then clips the points to a specific region.
# --------------------------------------------------------------------------------------

import arcpy
import os

#Set workspace
arcpy.env.workspace = r'C:\'

#Set the variables
points = r'C:\'
points_clip = r'C:\'
clip_features = r'C:\'
#List the rasters with names starting with v.
rasters = arcpy.ListRasters("v*", "TIF")

#For loop to go through the rasters and convert them, after clip them
for i in rasters:
    name = str(i)
    outPoint = points + "\\" + name[:3] + ".shp"
    arcpy.RasterToPoint_conversion(i, outPoint, "VALUE")
    out_feature_class = points_clip + "\\" + name[:3] + ".shp"
    arcpy.Clip_analysis(outPoint, clip_features, out_feature_class)


        
      
