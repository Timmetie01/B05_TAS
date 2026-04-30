import classes
import calculations
import matplotlib.pyplot as plt
import numpy as np
#np.set_printoptions(threshold=np.inf)

take_1 = classes.Data('take_001')
take_2 = classes.Data('take_002')
take_3 = classes.Data('take_003')
take_4 = classes.Data('take_004')
take_5 = classes.Data('take_005')


#Discretization?
#Base slipping?
#Markers not on arm tip??
#Wrong arm input?

take_3.plot_maneuver_duration(-20, 20)
take_3.plot_operations('arm_position', ('ma_filter_5', 'derivative_1'), (False, False, True), color='darkblue', label='arm_Z', showplot=False)
take_3.plot_operations('arm_position', ('ma_filter_5', 'derivative_1'), (False, True, False), color='darkorange', label='arm_Y', showplot=False)
take_3.plot_operations('arm_position', ('ma_filter_5', 'derivative_1'), (True, False, False), color='purple', label='arm_X', showplot=False)
plt.legend(fontsize=20)
plt.xlabel('newlabel', fontsize=15)
plt.ylabel('newlabel', fontsize=15)
plt.grid(True, ls='--')
plt.show()

#take_1.plot_operations('arm_position', ('derivative_0'), (True, True, True), color='darkblue', label='Arm', showplot=True)

take_3.plot_base_circle((True, True, True), showplot=False)

take_3.base_center_trajectory_reconstruction_2attempt((True, True, True))
take_3.plot_operations('base_position', ('derivative_0'), (True, True, True), color='purple', label='Base', showplot=False)
take_3.plot_trajectory_center(part='sections', XYZ=(True, True, True), color='#00B8C8', showplot=False, type='line', label='Trajectory Center')
take_3.plot_trajectory_center(part='target', XYZ=(True, True, True), color='darkorange', showplot=False, type='scatter', label='Target Center')
take_3.plot_operations('target', ('derivative_0'), (True, True, True), color='black', label='Target', showplot=False)
take_3.plot_waypoint_estimates((True, True, True), color='darkgreen', showplot=False)
take_3.plot_target_waypoints((True, True, True), color='firebrick', showplot=False)
take_3.plot_operations('arm_position', ('derivative_0'), (True, True, True), color='darkblue', label='arm', custom_axis_label=('X (mm)',None, 'Z (mm)'), showplot=False)
plt.legend(fontsize=12)
plt.grid(True, ls='--')
plt.show()

 

take_3.plot_waypoint_tracking_error(print_report=True, showplot=True)
#take_1.motion_capture_waypoint_error(True)
#take_2.motion_capture_waypoint_error(True)
#take_3.motion_capture_waypoint_error(True)
#take_3.motion_capture_waypoint_error(True)
#take_4.plot_waypoint_error(print_report=True, showplot=True)



#arm_noise = take_2.noise_covariance('arm_position')
#print(arm_noise)
