
#%%
import numpy as np
import pandas as pd
import os
import re # for regular expressions
import seaborn as sns #for graph in correlation heatmap
import matplotlib.pyplot as plt


#%%
#Set directory
os.chdir("C:/Users/Tim/Documents/GitHub/Master-Thesis/Baublatt Info")

def directory_maker(x):
    x_changed = os.path.normpath(x)
    x_final = os.path.join(os.getcwd(), x_changed)
    return x_final

def read_baublatt_pd(x):
    data = pd.read_csv(directory_maker(x),sep=';', na_filter=False, encoding='latin-1')
    return data

#%% Load the Data
#Files
path_2006_01 =  "Baublatt_data/2006_01_KOF_9943D2K.csv"
path_2006_01c = "Baublatt_data/KOF_9943D2K_2006_01_bereinigt.csv"
path_2007_01 =  "Baublatt_data/KOF_9943D2K_2007_01.csv"
path_2007_01c = "Baublatt_data/KOF_9943D2K_2007_01_bereinigt.csv"

BP_2006_01 = read_baublatt_pd(path_2006_01)

BP_2006_01c= read_baublatt_pd(path_2006_01c)

BP_2007_01 = read_baublatt_pd(path_2007_01)

BP_2007_01c = read_baublatt_pd(path_2007_01c)
#%% get the Adress from the form uncleaned set
# Form an own data frame for the adresses



#df2006 = pd.merge(BP_2006_01c,BP_2006_01[[var_adress]],on='ObjektNr', how='left')



#Final Frame is made here for the usage of the cleaned data, further it has been stack together
#df.Hausnummer = df.Baustelle.str.extract("[^ ]* (.*)") 

#Get Adress Frame to work with coordinates 
#adr_df = df[var_adress]



#%% # Define new Vars Lists which I will need  

#all vars needed
var_keep = ['ObjektNr',"Baustelle","BaustPlz", "BaustOrt","BausKanton",
            "BezirkCode","BaustSprache", "BezirkName",'Kurzbeschreibung',
            'BauartCode','Baubeginn','Bauende','GesuchVom','BewilligtAm',
             'BaukostenVon','BaukostenBis','AnzGeb','AnzWhg','AnzEtagen']

#vars added from the uncleaned data set RAW
var_needed = ['ObjektNr',"Baustelle","BaustPlz", "BaustOrt","BezirkCode",
            "BezirkName","BaustSprache"]

#vars needed from ALL
var_project_type = ["BauartCode", "AnzEtagen", "BaukostenBis", "AnzWhg", "AnzGeb"]

#vars needed from ALL
var_adress  = ['ObjektNr',"Baustelle","BaustPlz", "BaustOrt","BezirkCode",
            "BezirkName","BaustKanton","BaustSprache"]

#%%
#Create a bigger dataframe
df2006 = pd.merge(BP_2006_01c,BP_2006_01[var_needed],on='ObjektNr', how='left')
df2007 = pd.merge(BP_2007_01c,BP_2007_01[var_needed],on='ObjektNr', how='left')

#bring the data together
df = pd.concat([df2006,df2007], axis = 0)

#get only adress frame
adr_df = df[var_adress + var_project_type ]

#%%
list(df)
#%%
# 3.1 generate correlations between the housing type and if the map has house number

#3.2 get House number with Regex -> extract
"""Work here again on this number"""
HouseNumber = df.Baustelle.str.extract("[^ ]* (.*)")

#3.3 define the Columns als binary with House Number
df.HasHouseNumber = HouseNumber.isnull()

#3.4 get ratio of non-house number
HouseNumber.isna().sum()/len(HouseNumber)

#3.5 Decode the variable "BauartCode"
BauartCode_vec = df.BauartCode
BauartCode_ohe = pd.get_dummies(BauartCode_vec)

#Add Language
BaustSprache = pd.get_dummies(df.BaustSprache)

#Add Columns
BauartCode_ohe["Deutsch"] = BaustSprache.D
BauartCode_ohe["Italienisch"] = BaustSprache.I
BauartCode_ohe["Französisch"] = BaustSprache.F
BauartCode_ohe["HouseNumber"] = df.HasHouseNumber

#get heatmap
corr_Matrix = BauartCode_ohe.corr()
sns.heatmap(corr_Matrix, annot=True)
plt.show()

#sns.heatmap(pd.get_dummies(BauartCode_vec), annot=True)

    
#%%
#Write a function that defines 
# 1. Count if Bauat has Housenumber
# 2. Count if How often Bauart is there
# 3. Do this for the different languages
# 4. Work on regex
list = []
for i in np.arange(len(df)):
    # if bauart us 
    if df.BauartCode.values[i] == 1: j=1
    #if df.BauartCode.values[i] == 1 and if df.HasHouseNumber.values == True: o =1 
    else: j = 0
    list.append(j)
#%%
#df.groupby("BauartCode").size()
df.HasHouseNumber.values == True










