import pandas as pd
import numpy as np

def get_velocity_test_data():
    data = pd.read_csv('Velocitydatatest.csv')
    return pd.DataFrame.to_numpy(data)
