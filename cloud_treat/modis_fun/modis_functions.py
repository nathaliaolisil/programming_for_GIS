import os
import os.path
import arcpy
from datetime import datetime, date

#Copy Raster
def copyraster(temp, rasterlist, out_temp):
    for filename in rasterlist:
        name = str(filename)
        if name[:5] == "temp0":
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

#Find previous date file name
def prename(current_file, raster_list):
    position = (raster_list.index(current_file)) - 1
    name = str(raster_list[position])

    return name

#Find posterior date file name
def postname(current_file, raster_list):
    position = (raster_list.index(current_file)) + 1
    name = str(raster_list[position])

    return name

