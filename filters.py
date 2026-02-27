import numpy as np
import scipy as sp



def moving_averages(data, window_size, axis=0, extension_type='mirror'):
    '''
    Applies the moving averages filter along the specified axis of the input array, and outputs the filtered array
    Either 1D or 2D arrays possible as input
    
    :param data: 
    :param window_size: 
    :param axis: 0 or 1, along which axis should the input array be filtered
    :param extension_type: 'mirror' mirrors data near the ends over the ends, 'constant' repeats the outermost values, 'none' doesnt extend the input, thus reducing the output data by window_size - 1 entries. 
    :return filtered_data: The array with the filter applied. 
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

    #Apply the different extension types. Mirror mirrors the array at the ends, none just makes the output shorter. Constant repeats the values at the ends.
    if extension_type == "mirror":
        if len(data) < window_size:
            print('data matrix size should at least be as large as the window_size for meaningful results.')
            quit()
        extension_size = (window_size + 1)//2
        data = np.insert(data, 0, np.array(data[0:extension_size,:]), 0)
        data = np.insert(data, -1, np.array(data[-1 * extension_size:-1,:]), 0)

    elif extension_type == "constant":
        print('Constant extension type not implemented yet, sorry...')
        raise NotImplementedError
    
    elif extension_type == "none":
        pass

    else:
        print('choose correct extension type for moving_averages')
        quit()

    #Size the output matrix. If using extension, the data will be scaled up beforehand, and now scaled down again to original size.
    filtered_data = np.zeros((np.size(data, 0) - window_size + 1, np.size(data, 1)))
    
    #loop for taking the averages:
    #Basically taking certain length original samples, summing them over the correct axis and dividing over window_length, 
    #and entering that as the new data in another matrix
    for i in range(len(filtered_data)):
        filtered_data[i,:] = np.sum(data[i:i+window_size, :], axis=0) / window_size

    #Transpose the data if other axis is required. It was also flipped before the main part of this function, so is now back to normal.
    if axis == 1:
        filtered_data = np.transpose(filtered_data)
    return filtered_data


