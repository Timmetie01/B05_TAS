import graphing
import data_import
import filters
import classes
import time

data = classes.Data('test')

data.plot_ma_filter(51, derivative=0,  extension_type='mirror', difference=False, discrete_points=False)
