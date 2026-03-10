import graphing
import data_import
import filters
import classes
import time

take_1 = classes.Data('take_001')

take_1.plot_3D('base_position', window_size=21, filtered=True, end_plotting=False, target=True)
take_1.plot_3D('arm_position', window_size=21, filtered=True, start_plotting=False)

take_1.plot_3D('base_rotation', window_size=21, filtered=True, end_plotting=False)
take_1.plot_3D('arm_rotation', window_size=21, filtered=True, start_plotting=False)




