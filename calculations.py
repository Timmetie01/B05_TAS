import numpy as np
import time

def num_derivative(input_array, frequency, axis=0):
    '''
    Returns the numerical derivative of the input array along the specified axis. Default is vertically along 2d array
    For 250k datapoints, this function takes approximately 0.0014 seconds to run (first implementation: 0.5).
    
    :param input_array: 1d or 2d array of which the derivative should be taken along a specific axis
    :param frequency: the frequency (in Hz) of the measurements
    :param axis: Choose along which axis the derivative should be taken.

    :return output_array: The array of derivatives, structured similarly to the input_array
    '''
    if input_array.ndim > 2:
        print('More than 2 dimensions not implemented for derivative...')
        raise ValueError

    if axis == 1:
        input_array = np.transpose(input_array)

    #Initial mediocre implementation:
    #output_array = np.zeros_like(input_array)
    #for i in range(len(output_array)-1):
    #    output_array[i+1,:] = (input_array[i+1,:] - input_array[i,:])*frequency

    output_array = (input_array[2:,:] - input_array[:-2,:]) * frequency/2
    output_array = np.insert(output_array,  0, np.array([0] * len(output_array[0])), 0)
    output_array = np.insert(output_array, -1, np.array([0] * len(output_array[0])), 0)
    
    if axis == 1:
        output_array = np.transpose(output_array)

    return output_array
    
def find_center(input_points, radius):
    from scipy.optimize import minimize

    #[x, y, r]
    def squared_error(center=[0,0,0]):
        error = 0
        for i in input_points:
            error += (np.sqrt((i[0] - center[0]) ** 2 + (i[2] - center[1]) ** 2) - center[2]) ** 2

        return error
        
    result = minimize(squared_error, x0=[3000,2000, 1800])    
    x = result.x

    return np.array([x[0], np.average(input_points[:,1]), x[1]])




    