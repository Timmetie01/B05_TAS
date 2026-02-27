
class Data:
    def __init__(self, data_type):
        import data_import
        if data_type == 'test':
            self.values = data_import.get_velocity_test_data()
            


        #Set filtered values to None. These will be set once the filter is called the first time.
        #Afterwards, when called, it simply returns the variable instead of applying the filter again.
        self.ma_filtered_values = None

    def ma_filtered(self, window_size, axis=0, extension_type='none'):
        import filters
        #Apply the filter the first time it is called. After that, keep the filtered data such that it does not have to be recalculated.
        if self.ma_filtered_values == None:
            self.ma_filtered_values = filters.moving_averages(self.values, window_size, axis, extension_type)
            return self.ma_filtered_values
        else:
            return self.ma_filtered_values
        
    def plot_ma_filter(self, window_size, axis=0, extension_type='none', discrete_points=True, showplot=True):
        '''
        Plots the data after the moving averages filter and before

        :param window_size: The window size of the moving averages filter
        :param axis: Along which axis of the 2d data array the filter should be applied
        :param extension_type: currently only 'none' implemented
        :param discrete_points: If True, original data will be scattered. False gives a line.
        :param showplot: True calls plt.show(). False doesnt, and it will thus be layered under the next plot created
        '''
        import graphing
        shift = (window_size-1)/2 if extension_type == 'none' else 0
        graphing.test_filter(self.ma_filtered(window_size, axis, extension_type), self.values, discrete_points=discrete_points, filter_shift=shift, showplot=showplot)

    
        