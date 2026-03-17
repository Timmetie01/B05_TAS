import pandas as pd
import numpy as np

stored_numpy_arrays = np.load("AE2224-I_dataset/saved_data.npz", allow_pickle=True)

def get_velocity_test_data():
    #For reference: importing 250k test datapoints in a 1d array takes approximately 0.0364 seconds
    print("The velocity test data is outdated. Use the actual experiments pls")
    raise NotImplementedError

def get_data(filepath, header_size=0, right_cutoff=0):
    #If the user requests data stored in a numpy array, return that. If not, return file like normal
    if filepath[:24] == 'AE2224-I_dataset/take_00':
        index = f'take_00{filepath[24]}' 
        return stored_numpy_arrays[index]
    else:
        data = pd.read_csv(filepath)
        return pd.DataFrame.to_numpy(data)[header_size:,:-1 * right_cutoff]

def get_target_position(data_class, data_type):
    start_pos = data_class.arm_position[0,:]
    angle_arr = np.linspace(0, np.pi, len(data_class.arm_position[:,0]))
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

def save_data_arrays(header_size=0, right_cutoff=0):
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
    