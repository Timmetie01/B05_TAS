import classes
import calculations

take_1 = classes.Data('take_001')
take_2 = classes.Data('take_002')
take_3 = classes.Data('take_003')
take_4 = classes.Data('take_004')
take_5 = classes.Data('take_005')


'''
take_3.plot_maneuver_duration(-20, 20)
take_3.plot_operations('arm_position', ('derivative_1'), (False, False, True), color='darkblue', label='arm_Z', showplot=False)
take_3.plot_operations('arm_position', ('derivative_1'), (False, True, False), color='darkorange', label='arm_Y', showplot=False)
take_3.plot_operations('arm_position', ('derivative_1'), (True, False, False), color='purple', label='arm_X', showplot=True)

take_3.plot_operations('target', ('derivative_0'), (True, False, True), color='red', label='Target', showplot=False)
take_3.plot_waypoint_estimates((True, False, True), color='darkgreen', showplot=False)
take_3.plot_operations('arm_position', ('derivative_0'), (True, False, True), color='darkblue', label='arm', showplot=True)
'''

take_2.plot_operations('base_position', ('derivative_0'), (True, False, True), color='purple', label='Base', showplot=False)
take_2.plot_trajectory_center(part='sections', XYZ=(True, False, True), color='darkblue', showplot=False, type='line', label='Trajectory Center')
take_2.plot_trajectory_center(part='target', XYZ=(True, False, True), color='firebrick', showplot=False, type='scatter', label='Target Center')
take_2.plot_operations('target', ('derivative_0'), (True, False, True), color='firebrick', label='Target', showplot=False)
take_2.plot_waypoint_estimates((True, False, True), color='darkgreen', showplot=False)
take_2.plot_target_waypoints((True, False, True), color='firebrick', showplot=False)
take_2.plot_operations('arm_position', ('derivative_0'), (True, False, True), color='darkblue', label='arm', showplot=True)

'''
take_2.plot_operations('target', ('derivative_0'), (True, True, True), color='darkorange', label='Target', showplot=False)
take_2.plot_operations('arm_position', ('derivative_0'), (True, True, True), color='darkblue', label='Take 2', showplot=False)
take_3.plot_operations('arm_position', ('derivative_0'), (True, True, True), color='darkgreen', label='Take 3', showplot=False)
take_4.plot_operations('arm_position', ('derivative_0'), (True, True, True), color='firebrick', label='Take 4', showplot=True)
'''


'''
take_3.plot_operations('arm_position', ('derivative_1', 'ma_filter_11'), (True, True, True), color='darkblue', label='derivative first', showplot=True)
take_3.plot_operations('arm_position', ('ma_filter_11', 'derivative_1'), (True, True, True), color='firebrick', label='filter first', showplot=True)
take_3.plot_operations('arm_position', ('derivative_1'), (True, True, True), color='darkblue', label='derivative', showplot=False)
take_3.plot_operations('arm_position', ('ma_filter_11'), (True, True, True), color='firebrick', label='filter', showplot=True)
'''
 


