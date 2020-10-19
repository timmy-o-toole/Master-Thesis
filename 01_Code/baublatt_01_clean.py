# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 09:27:29 2020

@author: Tim
"""
import numpy as np
import pandas as pd
import os
import re # for regular expressions
import seaborn as sns #for graph in correlation heatmap
import matplotlib.pyplot as plt
import openpyxl
#%%

def directory_maker(y,x):
    x_changed = os.path.normpath(x)
    y_changed = os.path.normpath(y)
    x_final = os.path.join(os.getcwd(),y_changed, x_changed)
    return x_final

def read_baublatt_pd(x,y):
    data = pd.read_csv(directory_maker(x,y),sep=';', na_filter=False, encoding='latin-1')
    return data

#=====================================

"""
Input is Pandas Dataframe Columns 

Output is Numpy
    1 = Has House Number Included and 
    0 = Has no Housenumber included"""

def hasNumbers(input_pandas): #needs to be one column
    
    Numbers = np.zeros(len(input_pandas))
    
    for i in np.arange(len(input_pandas)):
        
        #check if there is a number in the Adress. True = Match = 1
        Numbers[i] = bool(re.search(r'\d', input_pandas.values[i]))
    return Numbers
#=============================================

"""
Input is (Dataframe, dataframe Col1, Datafarem Loaction)
col1 = X
col2 = Baustelle (something with numbers)
Important: the last input checks if it has a number inside
thus we look whats going on there"""

def House_Number_Matrix(df, dfcol1, dfcol2):
    
    #Bauart =col1
    #choose dataframe, unique values of frame
    frame = np.zeros([5,len(pd.unique(dfcol1))])
      
    for i in np.arange(len(pd.unique(dfcol1))):
    
        frame[0,i] = len(df.loc[(dfcol1 == pd.unique(dfcol1)[i])])
        frame[1,i] = len(df.loc[(dfcol1 == pd.unique(dfcol1)[i])  & (hasNumbers(dfcol2) ==1)])
        frame[2,i] = len(df.loc[(dfcol1 == pd.unique(dfcol1)[i])  & (hasNumbers(dfcol2) ==0)])
        frame[3,i] = round(frame[1,i]/frame[0,i],2)
        
        frame[4,i] = round(frame[0,i] / len(df),2)

    return pd.DataFrame(data=frame,index = ["Total","Has House Number","No House Number","Percentage Has Number", "Percentage of Tot"], columns=pd.unique(dfcol1)) 


#%%PATHS
#Home Path
os.chdir("C:/Users/Tim/Documents/GitHub/Master-Thesis")

bb_input = "02_Data/input/Baublatt_data"
bb_output= "02_Data/output"

# Data Paths
path_2006_01 =  "2006_01_KOF_9943D2K.csv"
path_2006_01c = "KOF_9943D2K_2006_01_bereinigt.csv"
path_2007_01 =  "KOF_9943D2K_2007_01.csv"
path_2007_01c = "KOF_9943D2K_2007_01_bereinigt.csv"

BP_2006_01 = read_baublatt_pd(bb_input,path_2006_01)
BP_2006_01c= read_baublatt_pd(bb_input,path_2006_01c)
BP_2007_01 = read_baublatt_pd(bb_input,path_2007_01)
BP_2007_01c = read_baublatt_pd(bb_input,path_2007_01c)

#%%
#all vars needed
var_keep = ['ObjektNr',"Baustelle","BaustPlz", "BaustOrt","BausKanton",
            "BezirkCode","BaustSprache", "BezirkName",'Kurzbeschreibung',
            'BauartCode','Baubeginn','Bauende','GesuchVom','BewilligtAm',
             'BaukostenVon','BaukostenBis','AnzGeb','AnzWhg','AnzEtagen']

#vars added from the uncleaned data set RAW
var_needed = ['ObjektNr',"Baustelle","BaustPlz", "BaustOrt","BezirkCode",
            "BezirkName","BaustSprache"]

#vars needed from ALL
var_project_type = ["BauartCode","CRBCode01", "AnzEtagen", "BaukostenBis", "AnzWhg", "AnzGeb"]

#vars needed from ALL
var_adress  = ['ObjektNr',"Baustelle","BaustPlz", "BaustOrt","BezirkCode",
            "BezirkName","BaustKanton","BaustSprache"]


#Create a bigger dataframe
df2006 = pd.merge(BP_2006_01c,BP_2006_01[var_needed],on='ObjektNr', how='left') #is cleaned frame
df2007 = pd.merge(BP_2007_01c,BP_2007_01[var_needed],on='ObjektNr', how='left') #is cleaned frame
#bring the data together
df = pd.concat([df2006,df2007], axis = 0) #refers to cleaned frame
#get only adress frame
adr_df = df[var_adress + var_project_type]


#add CBRCode
#%%
House_Number_Matrix(df, df.CRBCode01,  df.Baustelle)


#%%

