import graphing
import data_import
import filters
import classes

data = classes.Data('test')

data.plot_ma_filter(51,derivative=0,  extension_type='mirror')