import classes
import calculations

take_1 = classes.Data('take_001')
take_2 = classes.Data('take_002')
take_3 = classes.Data('take_003')
take_4 = classes.Data('take_004')
take_5 = classes.Data('take_005')


# take_3.plot_maneuver_duration(-20, 20)
# take_3.plot_operations('arm_position', ('derivative_1'), (False, False, True), color='darkblue', label='arm_Z', showplot=False)
# take_3.plot_operations('arm_position', ('derivative_1'), (False, True, False), color='darkorange', label='arm_Y', showplot=False)
# take_3.plot_operations('arm_position', ('derivative_1'), (True, False, False), color='purple', label='arm_X', showplot=True)


# take_3.plot_operations('target', ('derivative_0'), (True, False, True), color='red', label='Target', showplot=False)
# take_3.plot_waypoint_estimates((True, False, True), color='darkgreen', showplot=False)
# take_3.plot_operations('arm_position', ('derivative_0'), (True, False, True), color='darkblue', label='arm', showplot=True)

take_3.plot_trajectory_center(part='sections', XYZ=(True, True, True), color='blue', showplot=False, type='line')
take_3.plot_trajectory_center(part='target', XYZ=(True, True, True), color='red', showplot=False, type='scatter')


take_3.plot_operations('target', ('derivative_0'), (True, True, True), color='red', label='Target', showplot=False)
take_3.plot_waypoint_estimates((True, True, True), color='darkgreen', showplot=False)
take_3.plot_operations('arm_position', ('derivative_0'), (True, True, True), color='darkblue', label='arm', showplot=True)

