#---------------------------------------------------------------------------------------
# Script author:    Nathalia De La Fuente Oliveira
# Versions:         ArcGIS 10.2; Python 2.7.5
# Purpose:          The script goes through a group of csv file of data points to:
#                   - Find cluster in each one using MeanShift
#                   - Assings labels to the rows
#                   - Saves in a csv file a dataframe with the original data and its
#                   respective labels.
# --------------------------------------------------------------------------------------

import numpy as np
import pandas as pd
import os
from sklearn.cluster import MeanShift 

#Set the work folder path
folderPath = r'C:\'

#For loop to go through the folderPath and find the csv files
for filename in os.listdir(folderPath):  
    fullpath = os.path.join(folderPath, filename)  
    if os.path.isfile(fullpath):  
        basename, extension = os.path.splitext(fullpath)
        #If the file is a csv it creates a DataFrame for it
        if extension.lower() == ".csv":
            cls = filename[3:6]
            print(cls)
            filename = folderPath + filename
            csv = pd.read_csv(filename, delimiter=";", header=0)
            df = pd.DataFrame(csv)
            print (df)

            #Fiding clusters
            ms = MeanShift()
            ms.fit_predict(csv)
            labels = ms.labels_

            #Show the number of identified clusters 
            n_clusters_ = len(np.unique(labels))
            
            print("Number of estimated clusters:", n_clusters_)

            #Rename the labels
            dfl = pd.DataFrame(labels, columns = ['UCS'])
            L = []
            for i in dfl.iloc[:,0]:
                i = str(cls) + str(i)
                print(i)
                L.append(str(i))
                dff = pd.DataFrame(L, columns = ['UCS'])

            #Gather the labels dataframe to the previous dataframe 
            result = pd.concat([df, dff], axis=1, join_axes=[df.index])

            print (result)

            #Save the new dataframe
            result.to_csv(cls +'_cluster.csv', index=False)


