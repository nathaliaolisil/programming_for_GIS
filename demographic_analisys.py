#---------------------------------------------------------------------------------------
# Script author:    Nathalia De La Fuente Oliveira
# Versions:         ArcGIS 10.2; Python 2.7.5
# Purpose:          The script gives as an output the percentage of The Bronx population
#                   within the blocks 1/4 mile from the subway stations in NYC.
# --------------------------------------------------------------------------------------

import arcpy

# Overwrite existing output
arcpy.env.overwriteOutput = True

# Set workspace: database
arcpy.env.workspace = r'C:\'
wksp = arcpy.env.workspace

# Assign variables
Subway_Stations =  r'C:\' 
NYC_2010_CB_Dem =  r'C:\'
NYC_Borough_Boundaries = r'C:\'
print arcpy.Exists(Subway_Stations)

# Select BX by attribute
# Make feature layer
sql_Exp = ''' "BORONAME" = 'Bronx' '''
BX_lyr = arcpy.MakeFeatureLayer_management(NYC_Borough_Boundaries, "BX_lyr", sql_Exp)
print arcpy.GetCount_management(BX_lyr)

# Make BX seleciton permanent
BX_Boundary = arcpy.CopyFeatures_management(BX_lyr, "BX_Boundary")
print (arcpy.GetCount_management(BX_Boundary))

# Clip stations and census blocks to Bronx
BX_Stns_Clip = arcpy.Clip_analysis(Subway_Stations, BX_Boundary, "BX_Stns_Clip")
print (arcpy.GetCount_management(BX_Stns_Clip))

# Create ¼ mile buffers around subway stations.
BX_Stns_Buffer = arcpy.Buffer_analysis(BX_Stns_Clip, "BX_Stns_Buffer", "0.25 MILES", "", "", "ALL")
print (arcpy.GetCount_management(BX_Stns_Buffer))

# Intersect buffer with CB
BX_CB_Buffer = arcpy.Intersect_analysis([BX_Stns_Buffer, NYC_2010_CB_Dem], "BX_CB_Buffer", "ALL", "", "INPUT")
print (arcpy.GetCount_management(BX_CB_Buffer))

# Population in CB buffer
BX_CB_Buffer_Pop = arcpy.Statistics_analysis(BX_CB_Buffer, "BX_Buffer_Pop", [["POP", "SUM"]])
print (arcpy.GetCount_management(BX_CB_Buffer_Pop))

#Population in the Bronxs
BX_POP = arcpy.Statistics_analysis (NYC_2010_CB_Dem, "BX_Pop", [["POP", "SUM"]], "Borough code")
print (arcpy.GetCount_management())

#Join Bronxs population table and subway station table
arcpy.JoinField_management (BX_CB_Buffer_Pop, "Borough code", BX_POP, "Borough code", "SUM_POP")

#Add field to CB buffer population table
arcpy.AddField_management (BX_CB_Buffer_Pop, "Perc_POP", "FLOAT")

#Calculate percentage pop
arcpy.CalculateField_management (BX_CB_Buffer_Pop, "Perc_POP", "!SUM_POP! / !SUM_POP_1! *100", "PYTHON_9.3")
print (arcpy.GetCount_management())








