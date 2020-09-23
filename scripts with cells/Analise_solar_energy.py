# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import seaborn 

seaborn.set()
# %%
def read_file(file):
    try:
        print('Reading '+file)
        dataframe = pd.read_csv(file)
    except:
        print('Error: file not found.')
        sys.exit(1)
    else:
        print('Read complete.')
        dataframe = processing_data(dataframe)
        dataframe.info()
        return dataframe
# %%
def processing_data(dataframe):
    dataframe.DATE_TIME = dataframe.DATE_TIME.astype(np.datetime64)
    dataframe = dataframe.drop('PLANT_ID', axis=1)
    return dataframe
# %%
gen1 = read_file('../excel/solar_energy/Plant_1_Generation_Data.csv')
# %%
sen1 = read_file('../excel/solar_energy/Plant_1_Weather_Sensor_Data.csv')
# %%
cells1 = gen1.SOURCE_KEY.drop_duplicates().sort_values()
# %%
