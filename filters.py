import numpy as np
import scipy as sp



def moving_averages(data, window_size, axis=0, extension_type='mirror'):
    '''
    Applies the moving averages filter along the specified axis of the input array, and outputs the filtered array
    Either 1D or 2D arrays possible as input
    
    :param data: 
    :param window_size: 
    :param axis: 0 or 1, along which axis should the input array be filtered
    :param extension_type: 'mirror' mirrors data near the ends over the ends, 'none' doesnt extend the input, thus reducing the output data by window_size - 1 entries. 
    :return filtered_data: 
    '''
    #throw an error if the input data is more than 2 dimensional, since the current implementation will not work this way
    if len(np.shape(data)) > 2:
        print("moving_averages filter can only be applied on a 2d array of data. If you need this on higher dimensions, feel free to implement it.")
        quit()

    #ensuring symmetry in the window (current value, and equal amounts on left and right)
    if window_size // 2 != 1:
        window_size += 1

    #Transpose the data if other axis is required. Then, all code below can be the same, it just needs to be flipped back at the end of this function
    if axis == 1:
        data = np.transpose(data)

    #Apply the different extension types. Mirror mirrors the array at the ends, none just makes the output shorter
    if extension_type == "mirror":
        print('not implemented yet, sorry!')
        quit()
        if len(data) < window_size:
            print('data matrix size should at least be as large as the window_size for meaningful results.')
            quit()
        extension_size = (window_size - 1)//2
        data = np.insert(data, 0, data[0:window_size,:])
        data = np.insert(data, -1, data[-1 * data[0:window_size,:]:-1,:])
    elif extension_type == "none":
        pass
    else:
        print('choose correct extension type for moving_averages')
        quit()

    #Actually apply the filter
    filtered_data = apply_moving_average_filter(data, window_size)

    #Transpose the data if other axis is required. It was also flipped before the main part of this function, so is now back to normal.
    if axis == 1:
        filtered_data = np.transpose(filtered_data)
    return filtered_data


def apply_moving_average_filter(data, window_size):
    #Size the output matrix. 
    filtered_data = np.zeros((np.size(data, 0) - window_size + 1, np.size(data, 1)))

    #loop for taking the averages
    for i in range(len(filtered_data)):
        filtered_data[i,:] = np.sum(data[i:i+window_size, :], axis=0) / window_size

    return filtered_data

