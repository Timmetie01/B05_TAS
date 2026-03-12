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
        elif component == 'target':
            data = self.target_positions
        else:
            print("Choose available data to take derivative from!")
            raise ValueError
        return data
    
    

    def general_derivative(self, component, n, axis=0):
        '''
        Calculates the n'th derivative of the position. 

        :param component: Either 'base_position', 'base_rotation_deg', base_rotation_rad, 'arm_position', 'arm_rotation_deg', 'arm_rotation_rad' or target
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
    
    def plot_3D(self, component, default=True, filtered=False, window_size=1, target=False, showplot=True):
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
        graphing.trajectory_3d_plot(data if default else None, target=target_data, filtered=filtered_data, label=f'{component}', showplot=showplot)

    def plot_operations(self, component, operations, XYZ=(True, True, True), showplot=True, title=None, label='no_label', color=None):
        '''
        A function capable of plotting the data after an unlimited sequence of operations, such as derivatives and filters.

        :param component: Either 'base_position', 'base_rotation_deg', base_rotation_rad, 'arm_position', 'arm_rotation_deg', 'arm_rotation_rad' or 'target'
        :param operations: A tuple of operations in the order you want them executed. Possiblities: 'ma_filter_x' (x is window width), 'derivative_x'. Example ('ma_filter_5', 'derivative_2', 'ma_filter_11') for a filtered second order derivative of filtered data. Since it must be a tuple, if you only have one argument it must have a comma after it, i.e. (ma_filter_11,)
        :param XYZ: A tuple of booleans representing each axis. Set True all 3 for a 3d plot, select 2 out of 3 True and the other False for a 2d plot in that plane. Example (True, True, True) for 3d, (True, False, True) for X-Z plot
        :param showplot: Decide wether to show the plot or not. When not shown, you can fall this function again to plot something else on top of the previous plot.
        :param title: Specify a title (string) for the plot
        :param label: Give the thing you're currently plotting a name in the legend
        :param color: This one should be obvious. Preferred colors: 'darkblue', 'firebrick', 'darkgreen'. If more are needed make sure they are well visible and distinct.     
        
        '''
        import filters
        import calculations
        import graphing
        import matplotlib.pyplot as plt
        data = self.data_selection(component)

        if type(component) is not tuple:
            component = (component,)

        #Loop through the operations tuple, and perform each one.
        for i in operations:
            if i[0:10] == 'ma_filter_':
                data = filters.moving_averages(data, int(i[10:]))
            elif i[0:11] == 'derivative_':
                n = int(i[11:])
                for j in range(n):
                    data = calculations.num_derivative(data, self.frequency)
            else:
                print('\n\n**\t**\tChoose allowed operation, read the docstring for more information!**\t**\n\t\tAre you sure you made the operations a tuple by adding a comma?\n')
                raise ValueError
        

        #There's likely a smarter way to do this but this is easy
        if XYZ == (True, True, True):
            ax = graphing.get_ax(XYZ)
            ax.plot(data[:,0], data[:,1], data[:,2], label=label, color=color)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')

        elif XYZ == (True, True, False) :
            ax = graphing.get_ax(XYZ)
            ax.plot(data[:,0], data[:,1], label=label, color=color)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
        
        elif XYZ == (True, False, True):
            ax = graphing.get_ax(XYZ)
            ax.plot(data[:,0], data[:,2], label=label, color=color)
            ax.set_xlabel('X')
            ax.set_ylabel('Z')
            ax.xaxis.set_inverted(True)

        elif XYZ == (False, True, True):
            ax = graphing.get_ax(XYZ)
            ax.plot(data[:,1], data[:,2], label=label, color=color)
            ax.set_xlabel('Y')
            ax.set_ylabel('Z')

        else:
            print('Choose correct plot dimensions, either 3d or 2d allowed.')
            raise ValueError
        
        ax.set_title(title)

        if showplot:

            plt.gca().set_aspect('equal')
            plt.legend()
            plt.grid(True)
            plt.show()




