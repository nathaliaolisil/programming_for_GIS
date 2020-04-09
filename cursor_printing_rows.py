#------------------------------------------------------------------------------
# Script author:    Nathalia De Oliveira Silva
# Versions:         ArcGIS 10.2; Python 2.7.5
# Purpose:          The script does all of the following:
#                   - Create a search cursor for your dataset
#                   - Print out each row to the interpreter
#                   - Create a second search cursor
#                   - Using the second search cursor, print out the data
#                   values for each row of just two fields of your choosing
#                   to the interpreter
#                   - Create a third search cursor
#                   - For every row that the cursor is iterating over, print
#                   out the number of the row to the interpreter.
# -----------------------------------------------------------------------------

import arcpy
import os

# Overwrite existing output
arcpy.env.overwriteOutput = True

# Set the workspace path: database
arcpy.env.workspace = r"C:\"
wksp = arcpy.env.workspace

#Assign variable
Geomorphology = wksp + "\Geomorphology"

# Create a search cursor
cursor = arcpy.da.SearchCursor(Geomorphology, ["OBJECTID","Shape","Descrip","Area","Simbologia", "Litologia"])

#Print out each row to the interpreter
for row in cursor:
    print (row)
    
#Create the second search cursor
cursor2 = arcpy.da.SearchCursor(Geomorphology, ["Simbologia", "Litologia"])

#Print out the data values for each row of Simbologia and Litologia fields
for row in cursor2:
    print (row)

#Create the third search cursor
cursor3 = arcpy.da.SearchCursor(Geomorphology, ["Simbologia", "Litologia"])

#Print out the data values for each row of Simbologia and Litologia fields
i = 1
for row in cursor3:
    #print "Row: " + str(i)
    print ("Row {}".format(i) + " is printing")
    print (row[0], row[1])
    i += 1
print ("Script finished.")
