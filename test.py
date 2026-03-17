import classes
import time

take_1 = classes.Data('take_001')
take_2 = classes.Data('take_002')
take_3 = classes.Data('take_003')
take_4 = classes.Data('take_004')
take_5 = classes.Data('take_005')

#take_1.plot_operations('arm_position', ('ma_filter_1', 'derivative_1'), (True, False, True), color='darkblue', label='arm', showplot=False)
take_1.plot_operations('arm_position', ('ma_filter_31', 'derivative_1'), (False, True, False), color='firebrick', label='arm_filtered', showplot=True)
take_1.plot_operations('arm_position', ('ma_filter_31', 'derivative_0'), (False, True, False), color='darkblue', label='arm_filtered', showplot=True)
#take_1.plot_operations('target', ('ma_filter_1', 'derivative_0',),  (True, True, True), color='darkgreen', label='target', showplot=False)
#take_1.plot_operations('base_position', ('ma_filter_1', 'derivative_0'), (True, True, True), color='darkorange', label='base', showplot=False)
#take_1.plot_operations('base_position', ('ma_filter_50','derivative_0'), (True, True, True), color='purple', label='base_filtered', showplot=True)

