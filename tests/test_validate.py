import unittest
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
        data_update = data.copy()

        param_diff_len = [0, 5, 1]
        # requires func for test
        def error_func(data_update, param_diff_len):
            data_update['md'] = param_diff_len
            WellboreTrajectory(data_update)

        # create error raise
        with self.assertRaises(ValueError) as cm:
            error_func(data_update, param_diff_len)
        the_exception = cm.exception
        #print(the_exception.args[0])
        error_code = """Validation Error: Array lengths must be equal, md length: `3` inc length: `110` azim length: `110`"""
        self.assertEqual(the_exception.args[0], error_code)

        data_update = data.copy()
        param_diff_len = [0, 5, 1]
        # requires func for test
        def error_func(data_update, param_diff_len):
            data_update['inc'] = param_diff_len
            WellboreTrajectory(data_update)

        # create error raise
        with self.assertRaises(ValueError) as cm:
            error_func(data_update, param_diff_len)
        the_exception = cm.exception
        #print(the_exception.args[0])
        error_code = """Validation Error: Array lengths must be equal, md length: `110` inc length: `3` azim length: `110`"""
        self.assertEqual(the_exception.args[0], error_code)

        data_update = data.copy()
        param_diff_len = [0, 5, 1]
        # requires func for test
        def error_func(data_update, param_diff_len):
            data_update['azim'] = param_diff_len
            WellboreTrajectory(data_update)

        # create error raise
        with self.assertRaises(ValueError) as cm:
            error_func(data_update, param_diff_len)
        the_exception = cm.exception
        #print(the_exception.args[0])
        error_code = """Validation Error: Array lengths must be equal, md length: `110` inc length: `110` azim length: `3`"""
        self.assertEqual(the_exception.args[0], error_code)




#     def test_array_sign(self):
#
#         self.assertEqual(len([survey_obj.directional_survey_points.surface_longitude]), 1, 'incorrect')

#     def test_wellId(self):
#
#         self.assertEqual(len([survey_obj.directional_survey_points.surface_longitude]), 1, 'incorrect')

#     def test_lat_long_range(self):
#
#         self.assertEqual(len([survey_obj.directional_survey_points.surface_longitude]), 1, 'incorrect')

#     def test_array_monotonic(self):
#
#         self.assertEqual(len([survey_obj.directional_survey_points.surface_longitude]), 1, 'incorrect')


if __name__ == '__main__':
    unittest.main()
