import graphing
import data_import
import filters

data = data_import.get_velocity_test_data()
print(data)

window_size = 51
graphing.test_filter(filters.moving_averages(data, window_size, extension_type='none'), data, filter_shift=(window_size-1)/2)