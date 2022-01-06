#----------------------------------------------------------------------------------------
# Script author:    Nathalia De La Fuente Oliveira
# Versions:         ArcGIS 10.2; Python 2.7.5
# Purpose:          Tautomatize part of the methodology created by Geologos del mundo to
#                   calculate and map landslide susceptibility. 
# ---------------------------------------------------------------------------------------

# Import arcpy module
import arcpy
from arcpy import env
from arcpy.sa import *

# Check out any necessary licenses
arcpy.CheckOutExtension("Spatial")

# Overwrite existing output
arcpy.env.overwriteOutput = True

# Set the workspace path: database
arcpy.env.workspace = r""
wksp = arcpy.env.workspace

# Assign Variables
DEM = wksp + "\dem15_ixta_maza1"
Boundary = wksp + "\Boundary"
Landslides = wksp + "\Landslides"

# Perform Slope and save
Slope = Slope(DEM, "DEGREE", "1")
Slope.save("N:\")

#Perform Aspect and save
Aspect = Aspect(DEM)
Aspect.save("N:\")

# Reclassify Slope and Aspect rasters
Reclass_slope = Reclassify(Slope, "Value",RemapRange([[0,15,1],[15,30,2],[30,40,3],[40,50,4],[50,79,5]]))
Reclass_slope.save("N:\")

Reclass_aspect = Reclassify(Aspect, "Value",RemapRange([[-1,45,1],[45,135,2],[135,220,3],[220,315,4],[315,360,1]]))
Reclass_aspect.save("N:\")

#Convert reclassified rasters to polygon
Slope_poly = arcpy.RasterToPolygon_conversion(Reclass_slope, "G_slope_poly", "NO_SIMPLIFY","VALUE")
Aspect_poly = arcpy.RasterToPolygon_conversion(Reclass_aspect, "G_aspect_poly", "NO_SIMPLIFY","VALUE")

#Clip the polygons to the boudaries of the study area
Slope_clip = arcpy.Clip_analysis(Slope_poly, Boundary , "G_slope_clip")
Aspect_clip = arcpy.Clip_analysis(Aspect_poly, Boundary , "G_aspect_clip")

#Summarize the clipped layers to calculate the area of each grid code
Slope_area = arcpy.Statistics_analysis (Slope_clip, "G_slope_area", [["Shape_Area","SUM"]], ["gridcode"])
Aspect_area = arcpy.Statistics_analysis (Aspect_clip, "G_aspect_area", [["Shape_Area","SUM"]], ["gridcode"])

# Use identity to see how many landslides are within each grid code
Slope_identity = arcpy.Identity_analysis (Landslides, Slope_clip, "G_slope_ident")
Aspect_identity = arcpy.Identity_analysis (Landslides, Aspect_clip, "G_aspect_ident")

# Summarize the identity layers to count how many landslides there are within each grid code
Slope_landslides = arcpy.Statistics_analysis (Slope_identity, "G_slope_landslides", [["FID_Landslides","COUNT"]], ["gridcode"])
Aspect_landslides = arcpy.Statistics_analysis (Aspect_identity, "G_aspect_landslides", [["FID_Landslides","COUNT"]], ["gridcode"])

# Join the sumarized tables to have one table with the number of landslides within each category and the area
Slope_join = arcpy.JoinField_management (Slope_area,"gridcode",Slope_landslides, "gridcode", ["COUNT_FID_Landslides"])
Aspect_join = arcpy.JoinField_management (Aspect_area, "gridcode", Aspect_landslides, "gridcode", ["COUNT_FID_Landslides"])

# Add a field for the susceptibility numbers
Slope_field = arcpy.AddField_management (Slope_join, "Susc", "FLOAT")
Aspect_field = arcpy.AddField_management (Aspect_join, "Susc", "FLOAT")

# Use field calculator to calculate susceptibility numbers and normalize the results            
for i in [Slope_join, Aspect_join]:
    susc = arcpy.CalculateField_management (i, "Susc", "!COUNT_FID_Landslides!/!SUM_Shape_Area!", "PYTHON_9.3")
    cursor = arcpy.da.SearchCursor(i, ["gridcode", "Susc"])
    #Print out the data values of the Susc field rows of Slope and Aspect featureclass
    a = 1
    for row in cursor:
        if i == Slope_join:
            print ("Row {} of ".format(a) + "Slope")
            print ("Gridcode " + str(row[0]) + "  Susc " + str(row[1]))
            a += 1
            print ()
        else: 
            print ("Row {} of ".format(a) + "Aspect")
            print ("Gridcode " + str(row[0]) + "  Susc " + str(row[1]))
            a += 1
            print ()
print()

# Use field calculator to normalize the results 
arcpy.CalculateField_management (Slope_join, "Susc", "!Susc!/0.00005550203422899358",  "PYTHON_9.3")
arcpy.CalculateField_management (Aspect_join, "Susc", "!Susc!/0.00002684932951524388",  "PYTHON_9.3")

# Showing the results
for i in [Slope_area, Aspect_area]:
    cursor2 = arcpy.da.SearchCursor(i, ["gridcode","Susc"])
    #Print out the data values of the Susc and gridcode fields rows of Slope and Aspect featureclass
    a = 1
    for row in cursor2:
         if i == Slope_area:
            print ("Row {} of ".format(a) + "Slope")
            print ("Gridcode " + str(row[0]) + "  Susc " + str(row[1]))
            a += 1
            print ()
         else: 
            print  ("Row {} of ".format(a) + "Aspect")
            print ("Gridcode " + str(row[0]) + "  Susc " + str(row[1]))
            a += 1
            print ()





