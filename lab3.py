# A script to run the analysis for lab 3, GEOB 370.
# ArcMap/arcpy version 10.6.1, Python 2.7.14
# November 1, 2018
# This assumes all files are named as stated in the lab instructions. It will not work otherwise!

import os
import glob
from html.parser import HTMLParser
from bs4 import BeautifulSoup 
import numpy as np 
import pandas as pd 
import arcpy  
import arcpy.stats as stat
import arcpy.da


# Set your local variables.

workspace = r'C:\\GEOB370\\GEOB370_Lab3\\lab3'
# Skipped OLS for now (done by hand earlier). Will revisit. 

# Moran's I
# Where Moran's I evaluates whether a pattern is clustered, dispered, or 
# random.
# Positive Moran's I values, a p-value less than the desired confidence level and an abs(z-score) greater than the related p-value z score suggests strong  spatial autocorrelation and a rejection of the null hypothesis.

arcpy.env.workspace = workspace + r'\\MAUP.gdb'
arcpy.env.overwriteOutput = True

in_layers = ['VanDA_OLS', 'VanCT_OLS']
field = 'Residual'
out_html_list = []
os.chdir(workspace)
for layer in in_layers:
    arcpy.SpatialAutocorrelation_stats(layer, field, 'GENERATE_REPORT', 'INVERSE_DISTANCE', 'EUCLIDEAN_DISTANCE', 'NONE', '#')

    desc = arcpy.Describe(layer)
    layer_name = desc.nameString
    out_html_name = 'MoI_{}.html'.format(layer_name)
    os.rename(glob.glob(workspace + r'\\MoransI*.html')[0], out_html_name)
    out_html_list.append(out_html_name)
    print('Completed layer {}'.format(layer_name))

for doc in out_html_list:
    soup = BeautifulSoup(open(workspace + r'\\' + doc), 'html.parser')
    table = soup.find('table', attrs={'id':'keytable'})
    print(table.get_text())

# Layout: This is better done with ArcMap's GUI. Could potentially revisit creating this map programatically, but the script will likely be pretty extensive.

# Grouping Analysis
# Note: This doesn't work. Some unknown string error in the grouping analysis function call; potentially a bad variable type? Will need to investigate further.

in_layers = ['DA_Crimes', 'CT_Crimes']
unique_ID = 'OBJECTID'
analysis_fields = 'Tot_Private; MedHHInc; Count_; Sum_Auto_Theft; Sum_B_E_Resid; Sum_Mischief'

for layer in in_layers:

    desc = arcpy.Describe(layer)
    layer_name = desc.nameString
    stat.GroupingAnalysis_stats(layer, unique_ID, (workspace + '\\MAUP.gdb\\'+ layer_name[0:2] + '_grouping'), 4, analysis_fields, 'NO_SPATIAL_CONSTRAINT', 'EUCLIDEAN', '', '', , (workspace + '\\{}_grouping.pdf'.format(layer_name[0:2])) )

# Question 4: Finding where the CT doesn't represent the underlying variation in the DAs well.

# What we need to do:
#   Select all object IDs in the CT field, make a list. DONE
#   Iterate through the list, selecting each one then selecting the DAs by location.
#   Add the selected DAs to a pandas df w/ a column indicating the CT they belong to.
#   reset the selection of DAs before iterating again. 
#   Select the top two results. 
df_totals = pd.DataFrame() 

arcpy.SelectLayerByAttribute_management("CT_grouping")

with arcpy.da.SearchCursor("CT_grouping", "OBJECTID") as cursor:
    objectIDs = [row[0] for row in cursor]

    for i in objectIDs:
        # Selects each CT by objID
        arcpy.SelectLayerByAttribute_management(
                "CT_grouping",
                "NEW_SELECTION",
                '"OBJECTID" = ' + str(i))
        # Selects by location the DAs within
        current_area = arcpy.SelectLayerByLocation_management(
                "DA_grouping", 
                "WITHIN",
                "CT_grouping",
                0,
                "NEW_SELECTION"
                )
        # Returns values from the selected DAs as a np arr -> pandas df.
        # The temp dataframe is concatenated 
        fields = ["OBJECTID", "MedHHInc", "Sum_Auto_Theft", "Sum_B_E_Resid", "Sum_Mischief"]
        arr = arcpy.da.TableToNumPyArray("DA_grouping", fields)
        df = pd.DataFrame(arr)
        # Inserting the CT_OBJID to reselect the DAs later.
        df.insert(1, "CT_OBJID", i, allow_duplicates=True)
        # Adding the data to the main df
        df_totals = pd.concat([df_totals, df], ignore_index=True)

# Next step: data crunching.

#NOTE THAT THIS DOESN'T WORK
    for i in objectIDs:
        subset = df_totals.loc[df['CT_OBJID'] == i] # this line causes errors :'(
        foi = ["MedHHInc", "Sum_Auto_Theft", "Sum_B_E_Resid", "Sum_Mischief"]
        means = subset[foi].mean(axis=0)
        print("Mean of {} is {}".format(i, means))
        variance = subset[foi].var(axis=0)
        print("Variance of {} is {}".format(i, variance))