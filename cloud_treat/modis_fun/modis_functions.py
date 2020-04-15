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

#Rename MODIS bands to christian calendar
def rename(imagesworkspace):
    #Set workspace
    arcpy.env.workspace = imagesworkspace
    rasterlist = []
    rasters_tempr = arcpy.ListRasters("*R.tif", "TIF")
    rasters_tempn = arcpy.ListRasters("*N.tif", "TIF")
    rasters_tempndvi = arcpy.ListRasters("*NDVI.tif", "TIF")
    rasterlist.append(rasters_tempr)
    rasterlist.append(rasters_tempn)
    rasterlist.append(rasters_tempndvi)
    num = 1
    for rlist in rasterlist:
        
        if rlist != rasters_tempndvi:
            for r in rlist: 
                name = str(r)
                if name == rlist[-1]:
                    ()
                elif name != rlist[-1] and name != rlist[0]:
                    in_date = r
                    year = name[13:15]
                    d1 = datetime.strptime("20" + str(int(year)-1) + "1231","%Y%m%d")
                    idate = date.fromordinal(d1.toordinal()+ int(name[15:18]))
                    dateb = idate.strftime("%Y%m%d")
                    datec = dateb[2:8]
                    if name[18] == "R":
                        out_date = name[6:13] + "B" + str(num).zfill(3) + "RED" + datec
                        arcpy.Rename_management (in_date, out_date)
                        num = num + 1
                    if name[18:20] == "N.":
                        out_date = name[6:13] + "B" + str(num).zfill(3) + "NIR" + datec
                        arcpy.Rename_management (in_date, out_date)
                        num = num + 1
                
        else:
            for f in rlist:
                name = str(f)
                in_date = f
                year = name[13:15]
                d1 = datetime.strptime("20" + str(int(year)-1) + "1231","%Y%m%d")
                idate = date.fromordinal(d1.toordinal()+ int(name[15:18]))
                dateb = idate.strftime("%Y%m%d")
                datec = dateb[2:8]
                out_date = name[6:13] + "B" + str(num).zfill(3) + "NDV" + datec
                arcpy.Rename_management (in_date, out_date)
                num = num + 1

