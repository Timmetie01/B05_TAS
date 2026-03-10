import numpy as np
import time


class Data:
    def __init__(self, data_type):
        '''
        Sets up the data class for one of the measurement runs. 

        :param data_type: Specify which data to use. Either "test", or "take_00x" where x in [1,5]
        
        '''
        import data_import
        if data_type == "test":
            self.position = data_import.get_velocity_test_data()
            self.frequency = 350 #Hz
            print("Many things have changed since the last time the test data was used. It probably won't work anymore...")
        elif data_type[:-1] == "take_00":
            data = data_import.get_data(f"AE2224-I_dataset/{data_type}.csv", header_size=5, right_cutoff=10)
            #targets = data_import.get_data(f"AE2224-I_dataset/inputFile_00{data_type[-1]}.csv", header_size=0, right_cutoff=0)

            #Frame number must be an integer:
            self.frame = np.int64(np.array([data[:,0]]))
            
            #The rest of the array is still a string, so it must be converted to a float:
            data = np.float64(data)

            self.time = np.array([data[:,1]])
            self.base_rotation_deg = np.array(data[:,2:5])
            self.base_rotation_rad = self.base_rotation_deg * np.pi / 180
            self.base_position = np.array(data[:,5:8])
            self.arm_rotation_deg = np.array(data[:,8:11])
            self.arm_rotation_rad = self.arm_rotation_deg * np.pi / 180
            self.arm_position = np.array(data[:,11:14])
            self.frequency = 20  #Hz


            self.target_positions = data_import.get_target_position(self, data_type)

        else:
            print("Choose available data type!")
            raise ValueError
            
    def data_selection(self, component):
        if component == 'base_position':
            data = self.base_position
        elif component == 'base_rotation_deg':
            data = self.base_rotation_deg
        elif component == 'base_rotation_rad':
            data = self.base_rotation_rad 
        elif component == 'arm_position':
            data = self.arm_position  
        elif component == 'arm_rotation_deg':
            data = self.arm_rotation_deg  
        elif component == 'arm_rotation_rad':
            data = self.arm_rotation_rad  
        else:
            print("Choose available data to take derivative from!")
            quit()
        return data
    
    

    def general_derivative(self, component, n, axis=0):
        '''
        Calculates the n'th derivative of the position. 

        :param component: Either 'base_position', 'base_rotation_deg', base_rotation_rad, 'arm_position', 'arm_rotation_deg' or 'arm_rotation_rad'
        :param n: The order of the derivative
        :param axis: Along which axis the data matrix should be derived. Defaults to 0, which should almost always be correct.
        '''

        import calculations
        #I know many if statements is a lame way to implement this but it is quick enough for now
        data = self.data_selection(component)
        
        #Take the derivative n times.
        for i in range(n):
            data = calculations.num_derivative(data, self.frequency, axis)
        return data
    
    def plot_3D(self, component, default=True, filtered=False, window_size=1, target=False, start_plotting=True, end_plotting=True, dimensions=(True, True, True)):
        '''
        Creates a 3d plot of positional or rotational data

        :param component: Either 'base_position', 'base_rotation', 'arm_position' or 'arm_rotation'
        :param  default: Boolean, decides if the raw data should be plotted
        :param  filtered: Boolean, decides if the ma_filtered data should be plotted
        :param window_size: Integer, used when filtered=True to set window width of moving averages filter
        :param  target: Boolean, decides if the target data should be plotted
        :param showplot: True calls plt.show(). False doesnt, and it will thus be layered under the next plot created
        :param dimensions: 
        '''
        import graphing
        import filters
        if component == 'base_rotation':
            component = 'base_rotation_deg'
        elif component == 'arm_rotation':
            component = 'arm_rotation_deg'
        data = self.data_selection(component)
        filtered_data = filters.moving_averages(data, window_size, 0, 'mirror')  if filtered else None
        
        target_data = self.target_positions if target else None
        print(data)
        graphing.trajectory_3d_plot(data if default else None, target=target_data, filtered=filtered_data, label=f'{component}', start_plotting=start_plotting, end_plotting=end_plotting)

