# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 11:41:31 2020

@author: Tim
"""
#%%
import geopandas
import earthpy
import geopy

#%%
import numpy as np
import pandas as pd
import os
import re # for regular expressions
import seaborn as sns #for graph in correlation heatmap
import matplotlib.pyplot as plt
import openpyxl

#%% FUNCTIONS

def directory_maker(x):
    x_changed = os.path.normpath(x)
    x_final = os.path.join(os.getcwd(), x_changed)
    return x_final

def read_path_excel(x):
    data = pd.read_excel(directory_maker(x), na_filter=False)
    return data


#%% Load the Data
#Files
os.chdir("C:/Users/Tim/Documents/GitHub/Master-Thesis/Baublatt Info")
#
Adresse_df =  "data_adress.xlsx"
Adresse_df = read_path_excel(Adresse_df)

#%%
#locator = Nominatim(user_agent=”myGeocoder”)
#location = locator.geocode(“Champ de Mars, Paris, France”)
from geopy.geocoders import Nominatim

locator = Nominatim(user_agent="myGeocoder")

location = locator.geocode("Champ de Mars, Paris, France")

print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))