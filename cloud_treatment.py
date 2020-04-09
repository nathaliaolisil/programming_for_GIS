# Script author:    Nathalia De Oliveira Silva
# Versions:         ArcGIS 10.2; Python 2.7.5
# Purpose:          The script is part of the cloud treatment used in MODIS images.
# --------------------------------------------------------------------------------------

import arcpy
import os
import os.path
import shutil

#import the environment settings and spatial analyst extension

from arcpy import env
from arcpy.sa import *
from datetime import datetime, date

#Check out the Spatial Analyst extension
arcpy.CheckOutExtension("spatial")

# Set Work folder
folderPath = r"C://NOS//python_scripts//imagens//"

#Create directories
for i in range(3):
    os.mkdir(folderPath + '//temp0' + str(i))


# TASK 1 : COPY RASTER
#Set the workspace
arcpy.env.workspace = os.path.join(folderPath, "data")

#List all the .tif inside the folder data 
rasters = arcpy.ListRasters("masar*", "TIF")

#Set copy raster output folder
out_temp00 = os.path.join(folderPath, "temp00")

#Create a function to use the tool copyraster
def copyraster(temp, rasterlist, out_temp):
    for filename in rasterlist:
        name = str(filename)
        if name[:6] == "temp01":
            name = name[6:]
            #Set copy raster
            out_rasterdataset = os.path.join(out_temp, temp + name)
            #Execute copy raster
            arcpy.CopyRaster_management(filename,out_rasterdataset,"DEFAULTS","","", "NONE", "NONE", "16_BIT_UNSIGNED", "NONE", "NONE")
        else:
            
            #Set copy raster
            out_rasterdataset = os.path.join(out_temp, temp + name)
            #Execute copy raster
            arcpy.CopyRaster_management(filename,out_rasterdataset,"DEFAULTS","","", "NONE", "NONE", "16_BIT_UNSIGNED", "NONE", "NONE")
      
# Copy raster, pixel type to 16_BIT_UNSIGNED
copyraster("temp00", rasters, out_temp00)

print ("Copy raster done!")


# TASK 2: Calculate NDVI 16-bit: 65535 * n / (r + n)
# Set new workspace
arcpy.env.workspace = out_temp00

# List all the .tif inside the folder temp00
rasters_temp00 = arcpy.ListRasters("temp00*", "TIF")

#Set NDVI output folder
out_temp01 = os.path.join(folderPath, "temp01")

# Calculate NDVI
for j in rasters_temp00:
    name = str(j)
    if name == rasters_temp00[-1]:
        print ("NDVI done!")
    else:
        position = (rasters_temp00.index(j)) + 1
        name2 = str(rasters_temp00[position])
        #Set NDVI output
        out_ndvi = out_temp01 + "//" + "temp01" + name[6:18] + "NDVI" + ".tif"
        data1 = name[13:18]
        data2 = name2[13:18]
        if data1 == data2 :
            band1 = name[18]
            band2 = name2[18]
            if band1 == "N":
                red = name
                nir = name2
                #Calculate NDVI
                num = arcpy.sa.Float(arcpy.Raster(nir))
                denom = arcpy.sa.Float(arcpy.Raster(red)+arcpy.Raster(nir))
                eq = arcpy.sa.Divide(num, denom)
                ndvi = 65535 * eq
                ndvi.save(out_ndvi)
        else:
            ()    

# TASK 3: COPY RASTER

# Set new workspace
arcpy.env.workspace = out_temp01

# List all the .tif inside the folder temp02
rasters_temp01 = arcpy.ListRasters("temp01*", "TIF")

#Set copy raster output folder
out_temp02 = os.path.join(folderPath, "temp02")

# Copy raster, pixel type to 16_BIT_UNSIGNED
copyraster("temp02",rasters_temp01, out_temp02)

print ("Copy raster done!")


#TASK4: SUBTRACT PREVIOUS NDVI FROM EVERY DATE. SUBTRACT POSTERIOR NDVI FROM EVERY DATE.
# Set new workspace
arcpy.env.workspace = out_temp02

# List all the .tif inside the folder temp03
rasters_temp02 = arcpy.ListRasters("temp02*", "TIF")

#Set copy raster output folder
out_temp03 = os.path.join(folderPath, "temp03")

# Subtract previous and posterior ndvi from every date
for j in rasters_temp02:
    name = str(j)
    if name == rasters_temp02[-1]:
        print ("Subtraction done!")
    if name == rasters_temp02[0]:
        ()
    elif name != rasters_temp02[0] and name != rasters_temp02[-1]:
       
        anterior = (rasters_temp02.index(j)) - 1
        posterior = (rasters_temp02.index(j)) + 1
        
        name_ant = str(rasters_temp02[anterior])
        name_post = str(rasters_temp02[posterior])
        
        #Set output
        out_ant = out_temp03 + "//" + "temp03" + name[6:18] + "a.tif"
        out_post = out_temp03 + "//" + "temp03" + name[6:18] + "p.tif"
        #Execute subtraction
        sub_ant = arcpy.sa.Float(arcpy.Raster(name)-arcpy.Raster(name_ant))
        # Save the output 
        sub_ant.save(out_ant)
        #Execute subtraction
        sub_post = arcpy.sa.Float(arcpy.Raster(name)-arcpy.Raster(name_post))
        # Save the output 
        sub_post.save(out_post)


#TASK 05: RECLASSIFY
# Set new workspace
arcpy.env.workspace = out_temp03

# List all the .tif inside the folder temp04
rasters_temp03 = arcpy.ListRasters("temp03*", "TIF")

#Set copy raster output folder
out_temp04 = os.path.join(folderPath, "temp04")

# Reclassify images, negative values indicate cloud = C1
for k in rasters_temp03:
    name = str(k)
    #Set output
    out_reclass = out_temp04 + "//" + "temp04" + name[6:19] + "C1.tif"
    #Execute Reclassify
    reclass_nuv = arcpy.gp.Reclassify_sa(k, "Value",  "-65535 0 1;0 65535 0", out_reclass, "Data")

print("Reclassify done!")

print ("The End!")
