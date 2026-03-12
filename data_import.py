import pandas as pd
import numpy as np

def get_velocity_test_data():
    #For reference: importing 250k test datapoints in a 1d array takes approximately 0.0364 seconds.
    raise NotImplementedError
    data = pd.read_csv("Velocitydatatest.csv")
    return pd.DataFrame.to_numpy(data)

def get_data(filepath, header_size=0, right_cutoff=0):
    #Importing take 4 takes approximately 0.5 seconds. Optimization will be done later on, since this is too long.
    data = pd.read_csv(filepath)
    return pd.DataFrame.to_numpy(data)[header_size:,:-1 * right_cutoff]

def get_target_position(data_class, data_type):
    start_pos = data_class.arm_position[0,:]
    angle_arr = np.linspace(0, np.pi, 10000)
    target_pos = np.empty((len(angle_arr), 3))


    if data_type == 'take_001':
        r = 1600
    elif data_type == 'take_002' or data_type == 'take_003' or data_type == 'take_004':
        r = 2000
    elif data_type == 'take_005':
        r = 100000

    target_pos[:,0] = r * (np.cos(angle_arr) - 1)
    target_pos[:,2] = r * ( -1 * np.sin(angle_arr))
    target_pos += start_pos
    
    return target_pos
