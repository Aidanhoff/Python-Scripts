# A script to run the analysis for lab 3, GEOB 370.
# ArcMap/arcpy version 10.6.1, Python 2.7.14
# November 1, 2018
# This assumes all files are named as stated in the lab instructions. It will not work otherwise!

import os
import glob
from html.parser import HTMLParser
from bs4 import BeautifulSoup 
import arcpy  

# Set your local variables.

workspace = r'C:\GEOB370\GEOB370_Lab3\lab3'
# Moran's I
# Where Moran's I evaluates whether a pattern is clustered, dispered, or 
# random.
# Positive Moran's I values, a p-value less than the desired confidence level and an abs(z-score) greater than the related p-value z score suggests strong  spatial autocorrelation and a rejection of the null hypothesis.

arcpy.env.workspace = workspace + r'\MAUP.gdb'
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
    os.rename(glob.glob(workspace + r'\MoransI*.html')[0], out_html_name)
    out_html_list.append(out_html_name)
    print('Completed layer {}'.format(layer_name))

for doc in out_html_list:
    soup = BeautifulSoup(open(workspace + r'\\' + doc), 'html.parser')
    table = soup.find('table', attrs={'id':'keytable'})
    print(table.get_text())