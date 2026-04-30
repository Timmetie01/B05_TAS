import pandas as pd
import numpy as np

stored_numpy_arrays = np.load("AE2224-I_dataset/saved_data.npz", allow_pickle=True)

def get_velocity_test_data():
    #For reference: importing 250k test datapoints in a 1d array takes approximately 0.0364 seconds
    print("The velocity test data is outdated. Use the actual experiments pls")
    raise NotImplementedError

def get_data(filepath):
    #If the user requests data stored in a numpy array, return that. If not, return file like normal
    if filepath[:24] == 'AE2224-I_dataset/take_00':
        index = f'take_00{filepath[24]}' 
        return stored_numpy_arrays[index]
    else:
        data = pd.read_csv(filepath, header=None)
        return pd.DataFrame.to_numpy(data)

def get_target_position(data_class, data_type):
    start_pos = data_class.arm_position[0,:]
    angle_arr = np.linspace(0, np.pi, len(data_class.arm_position[:,0]))
    target_pos = np.zeros((len(angle_arr), 3))

    r = data_class.r

    target_pos[:,0] = r * (np.cos(angle_arr) - 1)
    target_pos[:,2] = r * ( -1 * np.sin(angle_arr))
    target_pos += start_pos

    return target_pos

def get_base_target(data_class, data_type):
    
    offset_vector = {
        '1':np.array([0, 0, 450.8]),
        '2':np.array([0, 0, 440.5]),
        '3':np.array([0, 0, 440.5]),
        '4':np.array([0, 0, 423.8])
    }

    total_rotation_of_base = {
        '1':3.0543262,
        '2':2.9321531,
        '3':2.9321531,
        '4':2.93448025
    }

    radii = {
        '1':1.727,
        '2':2.22,
        '3':2.22,
        '4':2.24
    }

    rotation = {
        '1':-0.1,
        '2':0.049,
        '3':0,
        '4':0
    }

    start_pos = data_class.base_position[0,:] + offset_vector[data_type[-1]]
    angle_arr = np.linspace(0, total_rotation_of_base[data_type[-1]], len(data_class.arm_position[:,0]))
    target_pos = np.zeros((len(angle_arr), 3))

    theta0 = rotation[data_type[-1]]
    r = radii[data_type[-1]] * 1000

    target_pos[:,0] = r * (np.cos(angle_arr) - 1)
    target_pos[:,2] = r * ( -1 * np.sin(angle_arr))
    return target_pos @ np.array([[np.cos(theta0),0, np.sin(theta0)], [0,1,0], [-1 * np.sin(theta0), 0, np.cos(theta0)]]) + start_pos

def save_data_arrays(header_size=5, right_cutoff=10):
    take_001 = pd.read_csv(f"AE2224-I_dataset/take_001.csv")
    take_001 = pd.DataFrame.to_numpy(take_001)
    take_002 = pd.read_csv(f"AE2224-I_dataset/take_002.csv")
    take_002 = pd.DataFrame.to_numpy(take_002)
    take_003 = pd.read_csv(f"AE2224-I_dataset/take_003.csv")
    take_003 = pd.DataFrame.to_numpy(take_003)
    take_004 = pd.read_csv(f"AE2224-I_dataset/take_004.csv")
    take_004 = pd.DataFrame.to_numpy(take_004)
    take_005 = pd.read_csv(f"AE2224-I_dataset/take_005.csv")
    take_005 = pd.DataFrame.to_numpy(take_005)

    np.savez("AE2224-I_dataset/saved_data", 
                take_001=take_001[header_size:,:-1 * right_cutoff],
                take_002=take_002[header_size:,:-1 * right_cutoff], 
                take_003=take_003[header_size:,:-1 * right_cutoff], 
                take_004=take_004[header_size:,:-1 * right_cutoff], 
                take_005=take_005[header_size:,:-1 * right_cutoff])

#When we get corrected or different data or something, the function below must be executed to renew saved numpy arrays
#save_data_arrays(5, 10)
    
    