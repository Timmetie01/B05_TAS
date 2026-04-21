import numpy as np
import time
import data_import


class Data:
    def __init__(self, data_type):
        '''
        Sets up the data class for one of the measurement runs. 

        :param data_type: Specify which data to use. Either "test", or "take_00x" where x in [1,5] 
        '''
        self.data_type = data_type
        if data_type == "test":
            self.position = data_import.get_velocity_test_data()
            self.frequency = 350 #Hz
            
        elif data_type[:-1] == "take_00":
            #WARNING: Due to how stored numpy arrays are implemented, the header size will not work there, but must be manually set in data_import.py 
            data = data_import.get_data(f"AE2224-I_dataset/{data_type}.csv")
            input_file = data_import.get_data(f"AE2224-I_dataset/inputFile_00{data_type[-1]}.csv")

            if data_type == 'take_001':
                self.r = 1600
            elif data_type == 'take_002' or data_type == 'take_003' or data_type == 'take_004':
                self.r = 2000
            elif data_type == 'take_005':
                self.r = 100000
            
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

            self.base_movement = np.array(input_file[:,1:4])
            self.arm_joint_targets = np.array(input_file[:,4:10])
            self.maneuver_duration = np.array(np.transpose([input_file[:,10]]))
            self.unknown_boolean_flag = np.array(np.transpose([input_file[:,11]]))

            self.target_positions = data_import.get_target_position(self, data_type)

            self.maneuver_start_index, self.maneuver_end_index = self.maneuver_start_end()
            self.maneuver_start_index, self.maneuver_end_index = np.asarray(np.round(self.maneuver_start_index * self.frequency), dtype=int), np.asarray(np.round(self.maneuver_end_index * self.frequency), dtype=int)

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
    
    def maneuver_start_end(self, stop_duration=1):

        if self.data_type == 'take_001': start_offset = 1.85
        elif self.data_type == 'take_002': start_offset = 6.75
        elif self.data_type == 'take_003': start_offset = 8.15
        elif self.data_type == 'take_004': start_offset = 2.7
        elif self.data_type == 'take_005': start_offset = 4.2
        else: start_offset = 0


        start_list = np.array([0])
        end_list = np.array([])
        for i, duration in enumerate(self.maneuver_duration[:,0]):


            if self.data_type == 'take_004' and duration == 10:
                end_list = np.append(end_list, start_list[-1] + duration + 0.025)
            else: 
                end_list = np.append(end_list, start_list[-1] + duration)
            
            start_list = np.append(start_list, end_list[-1] +  stop_duration)

        
        end_list = np.append(end_list, self.maneuver_duration[-1,0])
        start_list = np.delete(start_list, 0, 0)

        difference = 0
        #Remove the points halfway through a base maneuver
        for i in range(len(start_list)-5):
            i = i - difference
            
            #Any maneuver longer than 2 seconds is a base movement, and should waypoints with maneuvers longer than that before and after them should be removed. 3 is the cutoff to have some MoS from the 2
            if abs(end_list[i+1] - start_list[i]) > 3 and abs(end_list[i+2] - start_list[i+1]) > 3:
                end_list = np.delete(end_list, i+1)
                start_list = np.delete(start_list, i+1)
                difference += 1
                 
        
        start_list += start_offset
        end_list += start_offset


        return start_list, end_list

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

    def plot_operations(self, component, operations, XYZ=(True, True, True), showplot=True, title=None, label='no_label', color=None, custom_axis_label=(None, None, None)):
        '''
        A function capable of plotting the data after an unlimited sequence of operations, such as derivatives and filters.

        :param component: Either 'base_position', 'base_rotation_deg', base_rotation_rad, 'arm_position', 'arm_rotation_deg', 'arm_rotation_rad' or 'target'
        
        
        :param operations: A tuple of operations in the order you want them executed. \n
        Possiblities: \n
        'ma_filter_x' (x is window width), \n
        'derivative_x' (x is degree of derivative), \n
        None/'None'/'none' for nothing (i.e. placeholder), \n
        'threshold_filter_AB' (A is component (X, Y or Z), B is which derivative you want to use for the filter array (so use 1 if you want it filtered relative to velocity (which you should)). \n
        Example ('ma_filter_5', 'derivative_2', 'ma_filter_11') to calculate the second order derivative of data filtered with window width 5, and then filter the result with width 11.
        
        
        :param XYZ: A tuple of booleans representing each axis. Set True all 3 for a 3d plot, select 2 out of 3 True and the other False for a 2d plot in that plane, 1 True and 2 False for a single component vs time plot. Example (True, True, True) for 3d, (True, False, True) for X-Z plot, (True, False, False) for X-time plot.
        
        
        :param showplot: Decide wether to show the plot or not. When not shown, you can fall this function again to plot something else on top of the previous plot.
        
        
        :param title: Specify a title (string) for the plot
        
        
        :param label: Give the thing you're currently plotting a name in the legend
        
        
        :param color: This one should be obvious. Preferred colors: 'darkblue', 'firebrick', 'darkgreen'. If more are needed make sure they are well visible and distinct.     
        

        :param custom_axis_label: (str, str, str) Custom axis labels in order XYZ. Default None gives automatic labels. Can only be used in the same function call as where the plot is shown, otherwise the next plot will overwrite the custom labels.
        '''
        import filters
        import calculations
        import graphing
        import matplotlib.pyplot as plt
        data = self.data_selection(component)
        starting_data = data
        


        if type(operations) is not tuple:
            operations = (operations,)
        
        #Loop through the operations tuple, and perform each one.
        for i in operations:
            if i[0:10] == 'ma_filter_':
                data = filters.moving_averages(data, int(i[10:]))

            elif i[0:11] == 'derivative_':
                n = int(i[11:])
                for j in range(n):
                    data = calculations.num_derivative(data, self.frequency)

            elif i[0:17] == 'threshold_filter_':
                component = 0 if i[17] == 'X' else 1 if i[17] == 'Y' else 2 if i[17] == 'Z' else 3
                if component == 3:
                    raise ValueError
                
                filtering_array = np.transpose(np.array([starting_data[:,component]]))
                filtering_array = filters.moving_averages(filtering_array, 21)
                for j in range(int(i[18])):
                    filtering_array = calculations.num_derivative(filtering_array, self.frequency)

                #A horribly coded way to pass details through to the next function:
                data = filters.threshold_filter(self, data, filtering_array, component=f"{i[17:19]}{"bp" if component == "base_position" else "ap" if component == "arm_position" else "ar" if component  == "arm_rotation_deg" or component == "arm_rotation_rad" else "br" if component  == "base_rotation_deg" or component == "base_rotation_rad" else "ar"}")
                
            elif i == None or i == 'None' or i == 'none':
                continue
            else:
                print('\n\n**\t**\tChoose allowed operation, read the docstring for more information!\t**\t**\n\n')
                raise ValueError


        self.plot_different_dimensions(data, XYZ, color, label, title, custom_axis_label)
        
        if showplot:
            
            plt.legend()
            plt.grid(True, ls='--')
            plt.show()



    def plot_maneuver_duration(self,  ymin, ymax, stop_duration=1):
        import matplotlib.pyplot as plt

        start_list, end_list = self.maneuver_start_end(stop_duration)

        plt.vlines(start_list, ymin, ymax, color='green', label='Start maneuver')
        plt.vlines(end_list, ymin, ymax, color='red', label='End maneuver')


    def waypoint_positions(self, margin_from_maneuver=3, input_arr=None):
        #Take the average over the positions where the arm is not moving. THe starts and ends of maneuvers are already known, so this is simply an average taken below

        arr = input_arr if input_arr is not None else self.arm_position
    
        arm_waypoint_locations = list([arr[0,:]])
        for s, e in zip(self.maneuver_start_index, self.maneuver_end_index):
            
            arm_waypoint_locations.append(np.average(arr[e+margin_from_maneuver:s-margin_from_maneuver,:], 0))
            
        return np.array(arm_waypoint_locations)
    
    def target_waypoints(self):
        #Linearly space the amount of waypoints minus the amount of base movements to get the amount of unique target waypoints
        #Then, at the positions where the base moves, duplicate the target waypoint
        #This is because the measured waypoint before and after the maneuver should coincide
        waypoint_count = len(self.waypoint_positions())
        print('waypoint count:', waypoint_count)
        base_maneuvers = self.base_movement[:,0]
        base_maneuver_count = len(base_maneuvers[base_maneuvers != 0])

        start_pos = self.arm_position[0,:]
        angle_arr = np.linspace(0, np.pi, waypoint_count + base_maneuver_count)
        target_waypoint = np.zeros((len(angle_arr), 3))

        r = self.r

        target_waypoint[:,0] = r * (np.cos(angle_arr) - 1)
        target_waypoint[:,2] = r * ( -1 * np.sin(angle_arr))
        target_waypoint += start_pos

        print(len(target_waypoint))
        #To get the indices where the array should be doubled, use the input file and find the indices of its waypoints where the base moves
        indices = np.argwhere(self.base_movement[:,0])
        a = np.ones_like(indices)
        a[0,0] = 0
        indices = np.diff(indices, 1, 0, 0) - 1 - a
        indices = np.cumsum(indices, 0)
        indices = np.flip(indices, 0)
        print(indices)


        for i in indices[:,0]:
            target_waypoint = np.insert(target_waypoint, i, target_waypoint[i,:] + 5, axis=0)

        #print(target_waypoint)
        print(len(target_waypoint))
        return target_waypoint

    def plot_waypoint_estimates(self, XYZ=(True,True,True), type='scatter', showplot=True, label='Arm waypoints', title=None, color='darkblue', custom_axis_label=(None, None, None)):
        import matplotlib.pyplot as plt

        self.plot_different_dimensions(self.waypoint_positions(), XYZ, color=color, label=label, type=type, title=title, custom_axis_label=custom_axis_label)
        
        if showplot:
            plt.legend()
            plt.grid(True, ls='--')
            plt.show()

    def plot_target_waypoints(self, XYZ=(True,True,True), type='scatter', showplot=True, label='Target waypoints', title=None, color='firebrick', custom_axis_label=(None, None, None)):
        import matplotlib.pyplot as plt

        self.plot_different_dimensions(self.target_waypoints(), XYZ, color=color, label=label, type=type, title=title, custom_axis_label=custom_axis_label)
        
        if showplot:
            plt.legend()
            plt.grid(True, ls='--')
            plt.show()

    def plot_trajectory_center(self, XYZ=(True, True, True), part='sections', type='scatter', showplot=True, label='Trajectory Center', title=None, color='blue', custom_axis_label=(None,None,None)):
        '''
        Style should be 'total' or 'sections' or 'target'
        '''
        
        import matplotlib.pyplot as plt
        import calculations

        waypoints = self.waypoint_positions()


        if part == 'total':
            data = np.array([calculations.find_center(waypoints, self.r)])
        elif part == 'sections':
            self.maneuver_duration
            maneuvers = []
            
            maneuver_start = 0
            i = 0
            offset = 0
            while i < len(self.maneuver_duration):
                if self.maneuver_duration[i] > 2.1:
                    maneuvers.append(waypoints[maneuver_start - offset:i - 1 - offset,:])
                    offset += 2
                    maneuver_start = i
                    i += 2

                i += 1

            data = np.empty((len(maneuvers),3))

            for i in range(len(data)):
                data[i,:] = calculations.find_center(np.array(maneuvers[i]),self.r)

        elif part == 'target':
            start_location = self.arm_position[0,:]
            data = np.array([start_location - np.array([self.r, 0, 0])])

        else:
            print('Choose available trajectory center part. So either "total" for the entire half circle, or "sections" for each arm movement.')
            raise ValueError



        self.plot_different_dimensions(data, XYZ=XYZ, color=color, label=label, title=title, custom_axis_label=custom_axis_label, type=type)

        if showplot:
            plt.legend()
            plt.grid(True, ls='--')
            plt.show()

            
    def plot_different_dimensions(self, data, XYZ, color, label, title, custom_axis_label, type='line'):
        #Type is either line or scatter
        import graphing
        import matplotlib.pyplot as plt
        #There's likely a smarter way to do this but this is easy


        if XYZ == (True, True, True):
            ax = graphing.get_ax(XYZ)
            if type == 'line':
                ax.plot(data[:,0], data[:,1], data[:,2], label=label, color=color)
            elif type == 'scatter':
                ax.scatter(data[:,0], data[:,1], data[:,2], label=label, color=color)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            plt.gca().set_aspect('equal')

        elif XYZ == (True, True, False):
            ax = graphing.get_ax(XYZ)
            if type == 'line':
                ax.plot(data[:,0], data[:,1], label=label, color=color)
            elif type == 'scatter':
                ax.scatter(data[:,0], data[:,1], label=label, color=color)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            plt.gca().set_aspect('equal')
        
        elif XYZ == (True, False, True):
            ax = graphing.get_ax(XYZ)
            if type == 'line':
                ax.plot(data[:,0], data[:,2], label=label, color=color)
            elif type == 'scatter':
                ax.scatter(data[:,0], data[:,2], label=label, color=color)
            ax.set_xlabel('X')
            ax.set_ylabel('Z')
            ax.xaxis.set_inverted(True)
            plt.gca().set_aspect('equal')

        elif XYZ == (False, True, True):
            ax = graphing.get_ax(XYZ)
            if type == 'line': 
                ax.plot(data[:,1], data[:,2], label=label, color=color)
            elif type == 'scatter':
                ax.scatter(data[:,1], data[:,2], label=label, color=color)
            ax.set_xlabel('Y')
            ax.set_ylabel('Z')
            plt.gca().set_aspect('equal')

        elif XYZ == (True, False, False):
            ax = graphing.get_ax(XYZ)
            ax.plot(np.arange(len(data[:,0]))/self.frequency, data[:,0], label=label, color=color)
            ax.set_xlabel('time (s)')
            ax.set_ylabel('X')

        elif XYZ == (False, True, False):
            ax = graphing.get_ax(XYZ)
            ax.plot(np.arange(len(data[:,1]))/self.frequency, data[:,1], label=label, color=color)
            ax.set_xlabel('time (s)')
            ax.set_ylabel('Y')

        elif XYZ == (False, False, True):
            ax = graphing.get_ax(XYZ)
            ax.plot(np.arange(len(data[:,2]))/self.frequency, data[:,2], label=label, color=color)
            ax.set_xlabel('time (s)')
            ax.set_ylabel('Z')

        else:
            print('Choose correct plot dimensions, either 3d or 2d allowed.')
            raise ValueError
        
        if title is not None: ax.set_title(title)

        if custom_axis_label[0] is not None: ax.set_xlabel(custom_axis_label[0])
        if custom_axis_label[1] is not None: ax.set_ylabel(custom_axis_label[1])
        if custom_axis_label[2] is not None: ax.set_zlabel(custom_axis_label[2])




