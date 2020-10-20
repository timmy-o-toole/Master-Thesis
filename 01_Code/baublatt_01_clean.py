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
path_crb =  "CRBCodes.csv"

BP_2006_01 = read_baublatt_pd(bb_input,path_2006_01)
BP_2006_01c= read_baublatt_pd(bb_input,path_2006_01c)
BP_2007_01 = read_baublatt_pd(bb_input,path_2007_01)
BP_2007_01c = read_baublatt_pd(bb_input,path_2007_01c)
CRB_desc = read_baublatt_pd(bb_input, path_crb)

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
#adr_df = df[var_adress + var_project_type]


#add CBRCode
#%%
mat_cbr = House_Number_Matrix(df, df.CRBCode01,  df.Baustelle).T


#%%
# Use many cbr codes
# Wir nehmen nur Neubau//Abriss und andere Codes
# Read CBR Code Description // 



df_crb14  = df.loc[df.CRBCode01 == "14"]

#



#%% Perapre CRB Code

#drop Schuppen und Huetten = 41 ?
# 48 Jacuehgrube
# 51 Heizzentrale
# 52 Wasseraufbereitungsanlagen
#53	Kehrichtverbrennungs- und Wied
# 54 Tankstellen
# 55 Masten Tuerme
# 56 Waerme Kalteverteilung
# 57 Verteilanlagen
# 58 verteilanalgen Trinkwasser
# 113 Kantinen
# 118 Campinganalgen
# 122 Tribühnen
# 124 Reithallen
# 125 Bootshäuser
# 127 Spielpatz
#139 Garage
# Drop the above List here and type in the number what we do not need to use

#COND1: Drop_array 2 and the Numbers
#COND2: All numbers higher than 165
CRB_drop_array2 = [48, 51, 52, 53, 54, 55, 56, 57, 58, 113, 118, 122, 124, 125 , 127, 139]

#Final List of CRB Codes which are allowed
CRB_final= CRB_desc.loc[(CRB_desc.Number < 165) & (~CRB_desc.Number.isin(CRB_drop_array2))]

# List of all Numbers Which we will keep 
CRB_final_list = CRB_final.Number.tolist()


#============================================
#Desc Lists
# List of CRB Entries which we will keep
CRB_desc_keep = CRB_final.Desc.tolist()

# List of CRB Entries Which we have Deleted
CRB_desc_drop =    list(set(CRB_desc.Desc.tolist()) - set(CRB_desc_keep))




#%% Drop values from DF
#Drop Baucode 5 & 1
# Baucode 1 = NEUBAU
# Baucode 5 = ABRISS
#Drop CRB final



df["CRBCode01"] = pd.to_numeric(df["CRBCode01"])
df["BauartCode"] = pd.to_numeric(df["BauartCode"])

#Tranform column value first to numeric
df_final = df.loc[(df["CRBCode01"].isin(CRB_final_list)) & (df["BauartCode"].isin([1,5]))]


# use adaptive lasso to predict the house price and so to enh
#%%
mat_HouseNum_Kanton =  House_Number_Matrix(df_final, df_final.BaustKanton,  df_final.Baustelle).T
mat_houseNum_BaustSprach =  House_Number_Matrix(df_final, df_final.BaustSprache,  df_final.Baustelle).T
mat_houseNum_CBR =  House_Number_Matrix(df_final, df_final.CRBCode01,  df_final.Baustelle).T
mat_houseNum_CBR_uncleaned =  House_Number_Matrix(df, df.CRBCode01,  df.Baustelle).T


"""The average of housenumbers drops sharpley if the restrict to 
to Baucode 1/5 and if we restrict to the ther stuff"""
#write excel
#write Adress file
#load stuff first


