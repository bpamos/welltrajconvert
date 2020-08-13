import unittest
import random
from src.transforms import *
from src.wellbore_trajectory import *

current_dir = Path.cwd()
path = current_dir.parent
json_path = path/'data/wellbore_survey.json'

# Deserialize Json_Path
# with open(json_path) as json_file:
#     data = json.load(json_file)
# json_file.close()

file_path = get_files(path, folders='data', extensions='.json')
file_path = file_path.items[0]

# with open(json_path[0]) as json_file:
#     data = json.load(json_file)
# json_file.close()
#print(file_path)

# get survey obj
well_obj = WellboreTrajectory.from_json(file_path)
data = well_obj.data

class TestValidate(unittest.TestCase):

    def test_array_length(self):

        def errors(data_dict,key,param,error_code_str):
            # ERROR function
            # requires func for test
            def error_func(data_dict, param, key):
                data_update[key] = param
                WellboreTrajectory(data_update)

            # create error raise
            with self.assertRaises(ValueError) as cm:
                error_func(data_dict, param, key)
            the_exception = cm.exception
            #print(the_exception.args[0])
            error_code = error_code_str
            self.assertEqual(the_exception.args[0], error_code)

        # MD test
        # dict copy, for updating with error values for test
        data_update = data.copy()
        # key of interest
        key = 'md'
        # update dict values with errant data
        param = [0, 5, 1]
        #error code
        error_code_str = """Validation Error: Array lengths must be equal, md length: `3` inc length: `110` azim length: `110`"""
        # error function
        errors(data_update, key, param, error_code_str)

        # INC test
        # dict copy, for updating with error values for test
        data_update = data.copy()
        # key of interest
        key = 'inc'
        # update dict values with errant data
        param = [0, 5, 1]
        #error code
        error_code_str = """Validation Error: Array lengths must be equal, md length: `110` inc length: `3` azim length: `110`"""
        # error function
        errors(data_update, key, param, error_code_str)

        # AZIM test
        # dict copy, for updating with error values for test
        data_update = data.copy()
        # key of interest
        key = 'azim'
        # update dict values with errant data
        param = [0, 5, 1]
        #error code
        error_code_str = """Validation Error: Array lengths must be equal, md length: `110` inc length: `110` azim length: `3`"""
        # error function
        errors(data_update, key, param, error_code_str)




    def test_array_sign(self):

        def errors(data_dict,key,param,error_code_str):
            # ERROR function
            # requires func for test
            def error_func(data_dict, param, key):
                data_update[key] = param
                WellboreTrajectory(data_update)

            # create error raise
            with self.assertRaises(ValueError) as cm:
                error_func(data_dict, param, key)
            the_exception = cm.exception
            #print(the_exception.args[0])
            error_code = error_code_str
            self.assertEqual(the_exception.args[0], error_code)

        # dict copy, for updating with error values for test
        data_update = data.copy()
        # key of interest
        key = 'md'
        # update dict values with errant data
        param = list(np.array(data_update[key])*-1)
        #error code
        error_code_str = """Validation Error: MD array has negative values"""
        # error function
        errors(data_update, key, param, error_code_str)

        # dict copy, for updating with error values for test
        data_update = data.copy()
        # key of interest
        key = 'inc'
        # update dict values with errant data
        param = list(np.array(data_update[key])*-1)
        #error code
        error_code_str = """Validation Error: INC array has negative values"""
        # error function
        errors(data_update, key, param, error_code_str)



    def test_wellId(self):
        def errors(data_dict, key, param, error_code_str):
            # ERROR function
            # requires func for test
            def error_func(data_dict, param, key):
                data_update[key] = param
                WellboreTrajectory(data_update)

                print(data_update[key])

            # create error raise
            with self.assertRaises(TypeError) as cm:
                error_func(data_dict, param, key)
            the_exception = cm.exception
            #print(the_exception.args[0])
            error_code = error_code_str
            self.assertEqual(the_exception.args[0], error_code)


        # dict copy, for updating with error values for test
        data_update = data.copy()
        # key of interest
        key = 'wellId'
        # update dict values with errant data,
        param = 91
        # print(param)
        # error code
        error_code_str = """Validation Error: wellId has type <class 'int'>"""
        # error function
        errors(data_update, key, param, error_code_str)

        # dict copy, for updating with error values for test
        data_update = data.copy()
        # key of interest
        key = 'wellId'
        # update dict values with errant data,
        param = ['well_1','well_1','well_1']
        # error code
        error_code_str = """Validation Error: wellId has type <class 'list'>"""
        # error function
        errors(data_update, key, param, error_code_str)


    def test_lat_long_range(self):
        def errors(data_dict, key, param, error_code_str):
            # ERROR function
            # requires func for test
            def error_func(data_dict, param, key):
                data_update[key] = param
                WellboreTrajectory(data_update)

                print(data_update[key])

            # create error raise
            with self.assertRaises(ValueError) as cm:
                error_func(data_dict, param, key)
            the_exception = cm.exception
            #print(the_exception.args[0])
            error_code = error_code_str
            self.assertEqual(the_exception.args[0], error_code)

        # dict copy, for updating with error values for test
        data_update = data.copy()
        # key of interest
        key = 'surface_latitude'
        # update dict values with errant data,
        param = 91
        #print(param)
        # error code
        error_code_str = """Validation Error: surface_latitude has values outside acceptable range: 91"""
        # error function
        errors(data_update, key, param, error_code_str)

        # dict copy, for updating with error values for test
        data_update = data.copy()
        # key of interest
        key = 'surface_longitude'
        # update dict values with errant data,
        param = 190
        # error code
        error_code_str = """Validation Error: surface_longitude has values outside acceptable range: 190"""
        # error function
        errors(data_update, key, param, error_code_str)

    def test_array_monotonic(self):

        def errors(data_dict,key,param,error_code_str):
            # ERROR function
            # requires func for test
            def error_func(data_dict, param, key):
                data_update[key] = param
                WellboreTrajectory(data_update)

                print(data_update[key])

            # create error raise
            with self.assertRaises(ValueError) as cm:
                error_func(data_dict, param, key)
            the_exception = cm.exception
            #print(the_exception.args[0])
            error_code = error_code_str
            self.assertEqual(the_exception.args[0], error_code)

        # dict copy, for updating with error values for test
        data_update = data.copy()
        # key of interest
        key = 'md'
        # update dict values with errant data, update first 3 values in list to not monotoniclly increase
        param = data_update[key].copy()
        param[0:3] = [0.,40.,15.]
        # error code
        error_code_str = """Validation Error: MD array must monotonically increase"""
        # error function
        errors(data_update, key, param, error_code_str)

        # dict copy, for updating with error values for test
        data_update = data.copy()
        # key of interest
        key = 'md'
        # update dict values with errant data, reverse list to not monotoniclly increase
        param = data_update[key][::-1]
        # error code
        error_code_str = """Validation Error: MD array must monotonically increase"""
        # error function
        errors(data_update, key, param, error_code_str)


if __name__ == '__main__':
    unittest.main()
