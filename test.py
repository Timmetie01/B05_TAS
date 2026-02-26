import graphing
import data_import
import filters

data = data_import.get_velocity_test_data()
print(data)

graphing.test_filter(data, data)