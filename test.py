import classes
import time
import matplotlib.pyplot as plt
import numpy as np

take_1 = classes.Data('take_001')
take_2 = classes.Data('take_002')
take_3 = classes.Data('take_003')
take_4 = classes.Data('take_004')
take_5 = classes.Data('take_005')


#take_1.plot_operations('arm_position', ('ma_filter_41', 'derivative_0'), (True, True, True), color='firebrick', label='arm_MA', showplot=False)
#take_1.plot_operations('arm_position', ('ma_filter_41', 'threshold_filter_Y1', 'threshold_filter_X1','threshold_filter_Z1', 'derivative_0'), (True, True, True), color='darkblue', label='arm_threshold_filtered', showplot=True)


#plt.vlines(np.arange(0, 750, 3)+0.6, 500, 4500)
#plt.vlines(np.arange(0, 750, 3)+0.6, -20, 20, color='darkorange')
#plt.vlines(np.arange(0, 750, 3)-0.4, -20, 20, color='darkorange')


#take_3.plot_maneuver_duration(-20, 20)

take_3.plot_waypoint_estimates((True, True, True), color='darkgreen', showplot=False)
take_3.plot_operations('arm_position', ('ma_filter_1', 'derivative_0'), (True, True, True), color='darkblue', label='arm_Z', showplot=False)
take_3.plot_operations('arm_position', ('ma_filter_1', 'derivative_0'), (True, True, True), color='darkorange', label='arm_Y', showplot=False)
take_3.plot_operations('arm_position', ('ma_filter_1', 'derivative_0'), (True, True, True), color='purple', label='arm_X', showplot=True)


#take_1.plot_operations('base_position', ('ma_filter_1', 'derivative_0'), (False, False, True), color='darkorange', label='base_Z', showplot=False)
#take_1.plot_operations('base_position', ('ma_filter_1', 'derivative_0'), (False, True, False), color='yellow', label='base_Y', showplot=False)
#take_1.plot_operations('base_position', ('ma_filter_1', 'derivative_0'), (True, False, False), color='grey', label='basee_X', showplot=True)