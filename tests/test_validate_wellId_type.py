import unittest
from src.wellbore_trajectory import *

current_dir = Path.cwd()
path = current_dir.parent
json_path = path / 'data/wellbore_survey.json'

# get survey obj
well_obj = WellboreTrajectory.from_json(json_path)
data = well_obj.data


class TestValidateWellIdType(unittest.TestCase):

    def test_wellId_type(self):
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
            # print(the_exception.args[0])
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
        param = ['well_1', 'well_1', 'well_1']
        # error code
        error_code_str = """Validation Error: wellId has type <class 'list'>"""
        # error function
        errors(data_update, key, param, error_code_str)


if __name__ == '__main__':
    unittest.main()
