import graphing
import data_import
import filters
import classes
import time

take_1 = classes.Data('take_001')
'''
take_1.plot_3D('base_position', window_size=21, filtered=True, showplot=False, target=True)
take_1.plot_3D('arm_position', window_size=21, filtered=True, )

take_1.plot_3D('base_rotation', window_size=21, filtered=True, showplot=False)
take_1.plot_3D('arm_rotation', window_size=21, filtered=True)
'''

take_1.plot_operations('base_position', ('ma_filter_50', 'derivative_0',), (True, False, True), color='firebrick', label='base', showplot=False)
take_1.plot_operations('arm_position', ('ma_filter_50', 'derivative_0',), (True, False, True), title='Test_plot', color='darkblue', label='arm',showplot=True)

#take_1.plot_operations('arm_position', ('ma_filter_1', 'derivative_1',), title='Test_plot', color='firebrick', showplot=True)




