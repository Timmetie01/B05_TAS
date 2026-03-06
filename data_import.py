import pandas as pd
import numpy as np

def get_velocity_test_data():
    #For reference: importing 250k datapoints in a 1d array takes approximately 0.0364 seconds.
    data = pd.read_csv('Velocitydatatest.csv')
    return pd.DataFrame.to_numpy(data)
