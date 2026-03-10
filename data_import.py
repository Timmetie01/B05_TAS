import pandas as pd
import numpy as np

def get_velocity_test_data():
    #For reference: importing 250k test datapoints in a 1d array takes approximately 0.0364 seconds.
    data = pd.read_csv("Velocitydatatest.csv")
    return pd.DataFrame.to_numpy(data)

def get_data(filepath, header_size=0, right_cutoff=0):
    #Importing take 4 takes approximately 0.5 seconds. Optimization will be done later on, since this is too long.
    data = pd.read_csv(filepath)
    return pd.DataFrame.to_numpy(data)[header_size:,:-1 * right_cutoff]

