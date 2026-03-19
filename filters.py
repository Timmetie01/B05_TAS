import numpy as np
import scipy as sp

def moving_averages(data, window_size, axis=0, extension_type='mirror'):
    '''
    Applies the moving averages filter along the specified axis of the input array, and outputs the filtered array
    This function takes approximately 0.015 seconds to execute on 250k datapoints 

    
    :param data: Either 1D or 2D arrays possible as input which should be filtered
    :param window_size: The 'window' width, as used by the moving averages filter
    :param axis: 0 or 1, along which axis should the input array be filtered
    :param extension_type: 'mirror' mirrors data near the ends over the ends, 'constant' repeats the outermost values, 'none' doesnt extend the input, thus reducing the output data by window_size - 1 entries. 
    :return filtered_data: The array with the filter applied. 
    '''
    #throw an error if the input data is more than 2 dimensional, since the current implementation will not work this way
    if data.ndim > 2:
        print("moving_averages filter can only be applied on a 2d array of data. If you need this on higher dimensions, feel free to implement it.")
        raise ValueError

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
            raise ValueError
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
        raise ValueError

    #Size the output matrix. If using extension, the data will be scaled up beforehand, and now scaled down again to original size.
    filtered_data = np.zeros((np.size(data, 0) - window_size, np.size(data, 1)))
    
    #Summing the data matrix with the offset before dividing it by window size, effectively taking averages
    for i in range(window_size):
        filtered_data += data[i:(-window_size + i),:]
    
    #Original iterative implementation (100x slower)
    #for i in range(len(filtered_data))
        #filtered_data[i,:] = np.sum(data[i:i+window_size, :], axis=0) / window_size

    filtered_data = filtered_data / (window_size)
    #Transpose the data if other axis is required. It was also flipped before the main part of this function, so is now back to normal.
    if axis == 1:
        filtered_data = np.transpose(filtered_data)
    return filtered_data

def threshold_filter(data_class, data, filtering_array, threshold_value=-1, interpolate='linear', return_where_filtered=False, component='Y1ap'):
    '''
    Applies a threshold filter and interpolates the removed data.

    :param data: The full array of which the values must be removed
    :param filtering_array: The array on which the threshold filter is run, to decide which lines to remove from full array
    :param threshold_value: The absolute value above which a datapoint should be removed. -1 means automatic
    :param interpolate: the interpolation type, 'linear'
    :param return_where_filtered: When true, this function also returns the array of booleans that indicate where values have been filtered.
    :param component: The component currently taken as filtered array used to set thresholds, X0ap (X, Y, Z) direction + (0, 1, ...) derivative + (a, b) arm or base + (p, r) position or rotation
    '''
    
    if threshold_value == -1:
        data_type = data_class.data_type
        if data_type == 'take_001': 
            if   component == 'X1ap': threshold_value = (2.5, -2.5)
            elif component == 'Y1ap': threshold_value = (2.5, -2.5)
            elif component == 'Z1ap': threshold_value = (2.5, -2.5)
            elif component == 'X1ar': threshold_value = (2.5, -2.5)
            elif component == 'Y1ar': threshold_value = (2.5, -2.5)
            elif component == 'Z1ar': threshold_value = (2.5, -2.5)
            elif component == 'X1bp': threshold_value = (2.5, -2.5)
            elif component == 'Y1bp': threshold_value = (2.5, -2.5)
            elif component == 'Z1bp': threshold_value = (2.5, -2.5)
            elif component == 'X1br': threshold_value = (2.5, -2.5)
            elif component == 'Y1br': threshold_value = (2.5, -2.5)
            elif component == 'Z1br': threshold_value = (2.5, -2.5) 
        elif data_type == 'take_002': 
            if   component == 'X1ap': threshold_value = (2.5, -2.5)
            elif component == 'Y1ap': threshold_value = (2.5, -2.5)
            elif component == 'Z1ap': threshold_value = (2.5, -2.5)
            elif component == 'X1ar': threshold_value = (2.5, -2.5)
            elif component == 'Y1ar': threshold_value = (2.5, -2.5)
            elif component == 'Z1ar': threshold_value = (2.5, -2.5)
            elif component == 'X1bp': threshold_value = (2.5, -2.5)
            elif component == 'Y1bp': threshold_value = (2.5, -2.5)
            elif component == 'Z1bp': threshold_value = (2.5, -2.5)
            elif component == 'X1br': threshold_value = (2.5, -2.5)
            elif component == 'Y1br': threshold_value = (2.5, -2.5)
            elif component == 'Z1br': threshold_value = (2.5, -2.5)             
        elif data_type == 'take_003': 
            if   component == 'X1ap': threshold_value = (0, -2.5)
            elif component == 'Y1ap': threshold_value = (2.5, -2.5)
            elif component == 'Z1ap': threshold_value = (2.5, -2.5)
            elif component == 'X1ar': threshold_value = (2.5, -2.5)
            elif component == 'Y1ar': threshold_value = (2.5, -2.5)
            elif component == 'Z1ar': threshold_value = (2.5, -2.5)
            elif component == 'X1bp': threshold_value = (2.5, -2.5)
            elif component == 'Y1bp': threshold_value = (2.5, -2.5)
            elif component == 'Z1bp': threshold_value = (2.5, -2.5)
            elif component == 'X1br': threshold_value = (2.5, -2.5)
            elif component == 'Y1br': threshold_value = (2.5, -2.5)
            elif component == 'Z1br': threshold_value = (2.5, -2.5)              
        elif data_type == 'take_004': 
            if   component == 'X1ap': threshold_value = (2.5, -2.5)
            elif component == 'Y1ap': threshold_value = (2.5, -2.5)
            elif component == 'Z1ap': threshold_value = (2.5, -2.5)
            elif component == 'X1ar': threshold_value = (2.5, -2.5)
            elif component == 'Y1ar': threshold_value = (2.5, -2.5)
            elif component == 'Z1ar': threshold_value = (2.5, -2.5)
            elif component == 'X1bp': threshold_value = (2.5, -2.5)
            elif component == 'Y1bp': threshold_value = (2.5, -2.5)
            elif component == 'Z1bp': threshold_value = (2.5, -2.5)
            elif component == 'X1br': threshold_value = (2.5, -2.5)
            elif component == 'Y1br': threshold_value = (2.5, -2.5)
            elif component == 'Z1br': threshold_value = (2.5, -2.5)               
        elif data_type == 'take_005': raise ValueError
    else: threshold_value = (abs(threshold_value), -1 * abs(threshold_value))

    filter_boolean = (filtering_array > threshold_value[0]) | (filtering_array < threshold_value[1])

    #Converting from T/F to 1/0, and getting the elementwise difference. Also append 0 to start since the first value doesnt have a difference defined
    filter_binary = filter_boolean.astype(int)
    difference = np.diff(filter_binary, axis=0)
    difference = np.insert(difference, 0, 0)

    #If the difference between previous and current element is not zero, a filter is started or stopped
    filter_start = np.where(difference == 1)[0] + 1
    filter_end = np.where(difference == -1)[0] + 1

    if filter_binary[0]:
        filter_start = np.insert(filter_start, 0, 0)
    if filter_binary[-1]:
        filter_end = np.append(filter_end, len(filter_binary)-1)

    #Iterate over each stretch of filtered data. Delete the parts where the filter would be applied on 50 or less datapoints
    i = 0
    for s, e in zip(filter_start, filter_end):
        if e - s < 50:
            filter_start = np.delete(filter_start, i, 0)
            filter_end = +++np.delete(filter_end, i, 0)
        else: i += 1

    #Iterate over the stretches where there is no filter, to remove the parts where the filter momentarily turns off to avoid oscillation
    i = 0
    for s, e in zip(filter_start[1:], filter_end[:-1]):
        if s - e < 80:
            filter_start = np.delete(filter_start, i + 1, 0)
            filter_end = np.delete(filter_end, i, 0)
        else: i += 1

    #Apply the filter and interpolate .
    for s, e in zip(filter_start, filter_end):
        if interpolate == 'linear':
            for i in range(len(data[0,:])):

                data[s:e,i] = np.linspace(data[s,i], data[e,i], e-s, endpoint=True)
        else:
            print('Only linear interpolation for threshold filter currently implemented...')
            raise ValueError


    if return_where_filtered:
        return data, filter_boolean
    else: 
        return data



    
    
        
        
    

