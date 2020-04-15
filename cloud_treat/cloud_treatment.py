import arcpy
import os
from modis_fun import modis_functions as mf

#Check out the Spatial Analyst extension
arcpy.CheckOutExtension("spatial")

# Set Work folder
folderPath = r"C://NOS//python_scripts//imagens//"

#Create directories
for i in range(4):
    os.mkdir(folderPath + '//temp' + str(i).zfill(2))

# TASK 1 : COPY RASTER

#Set the workspace
arcpy.env.workspace = os.path.join(folderPath, "data")

#List all the .tif inside the folder data 
rasters = arcpy.ListRasters("masar*", "TIF")

#Set copy raster output folder
out_temp00 = os.path.join(folderPath, "temp00")

# Copy raster, pixel type to 16_BIT_UNSIGNED
mf.copyraster("temp00", rasters, out_temp00)

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
        name2 = mf.postname(j,rasters_temp00)
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

# List all the .tif inside the folder temp01
rasters_temp01 = arcpy.ListRasters("temp01*", "TIF")

#Set copy raster output folder
out_temp02 = os.path.join(folderPath, "temp02")

# Copy raster, pixel type to 16_BIT_UNSIGNED
mf.copyraster("temp02",rasters_temp01, out_temp02)

print ("Copy raster done!")

#TASK4: SUBTRACT PREVIOUS NDVI FROM EVERY DATE. SUBTRACT POSTERIOR NDVI FROM EVERY DATE.
# Set new workspace

arcpy.env.workspace = out_temp02

# List all the .tif inside the folder temp02
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
        name_ant = mf.prename(j,rasters_temp02)
        name_post = mf.postname(j,rasters_temp02)
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
