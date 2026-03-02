import numpy as np


class Data:
    def __init__(self, data_type):
        import data_import
        if data_type == 'test':
            self.position = data_import.get_velocity_test_data()
            self.frequency = 350 #Hz
        else:
            print("Choose available data type!")
            quit()
            

        #Set values to None. These will be set once the filter or other calculation is called the first time.
        #Afterwards, when called, it simply returns the variable instead of applying the filter again. Efficiency!
        self.ma_filtered_values = None
        self.derivative = None
        self.second_derivative = None

    def velocity(self, axis=0):
        import calculations
        #Apply the derivative the first time it is called. After that, keep the velocity data such that it does not have to be recalculated.
        if self.derivative == None:
            self.derivative = calculations.num_derivative(self.position, self.frequency, axis)
            return self.derivative
        else:
            return self.derivative
        
    def acceleration(self, axis=0):
        import calculations
        #Apply the derivatives the first time it is called. After that, keep the acceleration data such that it does not have to be recalculated.
        if self.second_derivative == None:
            self.second_derivative = calculations.num_derivative(self.velocity(axis), self.frequency, axis)
            return self.second_derivative
        else:
            return self.second_derivative
        
    def generic_derivative(self, n, axis=0, array=None):
        '''
        Calculates the n'th derivative of the position 
        :param n: The order of the derivative
        :param axis: Along which axis the data matrix should be derived. Default to 0, should work almost always
        :param array: The input array. None defaults to self.position
        '''

        import calculations
        if array == None:
            data = self.position
        else:
            data = array
        for i in range(n):
            data = calculations.num_derivative(data, self.frequency, axis)
        return data
            

    def ma_filtered(self, window_size, axis=0, extension_type='none'):
        import filters
        #Apply the filter the first time it is called. After that, keep the filtered data such that it does not have to be recalculated.
        if self.ma_filtered_values == None:
            self.ma_filtered_values = filters.moving_averages(self.position, window_size, axis, extension_type)
            return self.ma_filtered_values
        else:
            return self.ma_filtered_values
        
    def plot_ma_filter(self, window_size, derivative=0, axis=0, extension_type='none', discrete_points=True, showplot=True):
        '''
        Plots the data after the moving averages filter and before

        :param window_size: The window size of the moving averages filter
        :param derivative: choose 0, 1st or 2nd derivative or a list of multiple of these
        :param axis: Along which axis of the 2d data array the filter should be applied
        :param extension_type: currently only 'none' implemented
        :param discrete_points: If True, original data will be scattered. False gives a line.
        :param showplot: True calls plt.show(). False doesnt, and it will thus be layered under the next plot created
        '''
        import graphing
        import filters

        #For each 
        for i in np.nditer([derivative]):

            y_array = self.generic_derivative(i, axis)

            shift = (window_size-1)/2 if extension_type == 'none' else 0
            graphing.test_filter(filters.moving_averages(y_array, window_size, axis, extension_type), y_array, discrete_points=discrete_points, filter_shift=shift, showplot=showplot)

    
        