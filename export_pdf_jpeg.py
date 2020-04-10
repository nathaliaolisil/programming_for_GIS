#-------------------------------------------------------------------------------
# Script author:    Nathalia De Oliveira Silva
# Versions:         ArcGIS 10.2; Python 2.7.5
# Purpose:          The script export to PDF and JPG a group of .mxd files
#                   in a  folder.
# ------------------------------------------------------------------------------

import arcpy, os

#Set the input and output paths 
folderPath = r'C:\'
outpdf = r'C:\'
outjpg = r'C:\'

#For every mxd file in the folderPath export a pdf and a jpg file   
for filename in os.listdir(folderPath):

    #Split filename into basename and extension
    basename, extension = os.path.splitext(filename)

    #The variable fullpath is used to identify the filename path
    fullpath = os.path.join(folderPath, filename)

    #Check if it is a valid file
    if os.path.isfile(fullpath):  

        #If the extension is .mxd it export a pdf and a jpg file
        if extension == ".mxd":

            #Access the mxd file
            mxd = arcpy.mapping.MapDocument(fullpath)  

            #Export to pdf
            arcpy.mapping.ExportToPDF(mxd, outpdf + '\\' + basename + '.pdf', "", 0, 0, 500)

            #Export to jpg
            arcpy.mapping.ExportToJPEG(mxd, outjpg + '\\' + basename + '.jpg', resolution=500)
            



            

