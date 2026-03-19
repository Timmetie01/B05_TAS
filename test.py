import classes
import time



take_1 = classes.Data('take_001')
take_2 = classes.Data('take_002')
take_3 = classes.Data('take_003')
take_4 = classes.Data('take_004')
take_5 = classes.Data('take_005')


take_4.plot_operations('arm_position', ('ma_filter_41', 'derivative_0'), (True, True, True), color='firebrick', label='arm_MA', showplot=False)
take_4.plot_operations('arm_position', ('ma_filter_41', 'threshold_filter_Y1', 'threshold_filter_X1','threshold_filter_Z1', 'derivative_0'), (True, True, True), color='darkblue', label='arm_threshold_filtered', showplot=True)

take_4.plot_operations('arm_position', ('ma_filter_41', 'derivative_0'), (False, False, True), color='darkgreen', label='arm_Z', showplot=False)
take_4.plot_operations('arm_position', ('ma_filter_41', 'derivative_0'), (False, True, False), color='yellow', label='arm_Y', showplot=False)
take_4.plot_operations('arm_position', ('ma_filter_41', 'derivative_0'), (True, False, False), color='grey', label='arm_X', showplot=False)

take_4.plot_operations('arm_position', ('ma_filter_41', 'threshold_filter_Y1', 'threshold_filter_X1','threshold_filter_Z1', 'derivative_0'), (False, False, True), color='darkblue', label='arm_threshold_filtered_Z', showplot=False)
take_4.plot_operations('arm_position', ('ma_filter_41', 'threshold_filter_Y1', 'threshold_filter_X1','threshold_filter_Z1', 'derivative_0'), (False, True, False), color='darkorange', label='arm_threshold_filtered_Y', showplot=False)
take_4.plot_operations('arm_position', ('ma_filter_41', 'threshold_filter_Y1', 'threshold_filter_X1','threshold_filter_Z1', 'derivative_0'), (True, False, False), color='purple', label='arm_threshold_filtered_X', showplot=True)



