#from src.core import *
from src.directional_survey import *
import unittest

class TestRead(unittest.TestCase):

# TYPE ERRORS, md, inc, azim, wellid, surface lat and lon must be present
    def test_md_is_present(self):
        # md, inc, and azim can not have negative values, should throw error

        current_dir = Path.cwd()
        path = current_dir.parent / 'data'
        json_path = path / 'wellbore_survey.json'

        with open(json_path) as json_file:
            data = json.load(json_file)
        json_file.close()

        # create directional survey object
        # requires func for test
        def error_func(data):
            DirectionalSurvey(wellId=data['wellId'],
                              inc=np.array(data['inc']),
                              azim=np.array(data['azim']),
                              surface_latitude=data['surface_latitude'],
                              surface_longitude=data['surface_longitude']
                              )

        # create error raise
        with self.assertRaises(TypeError) as cm:
            error_func(data)
        the_exception = cm.exception
        #print(the_exception.args[0])
        error_code = """__init__() missing 1 required positional argument: 'md'"""
        self.assertEqual(the_exception.args[0], error_code)


# VALUES ARE NOT INTS
    def test_md_is_not_int(self):
        # md, inc, and azim can not have negative values, should throw error

        current_dir = Path.cwd()
        path = current_dir.parent / 'data'
        json_path = path / 'wellbore_survey.json'

        with open(json_path) as json_file:
            data = json.load(json_file)
        json_file.close()

        # convert param to int for error
        param_int = 1

        # create directional survey object
        # requires func for test
        def error_func(data, inc_int):
            DirectionalSurvey(wellId=data['wellId'],
                          md=param_int,
                          inc=np.array(data['inc']),
                          azim=np.array(data['azim']),
                          surface_latitude=data['surface_latitude'],
                          surface_longitude=data['surface_longitude']
                          )
        # create error raise
        with self.assertRaises(ValueError) as cm:
            error_func(data, param_int)
        the_exception = cm.exception
        #print(the_exception.args[0])
        error_code = """The field `md` was assigned by `<class 'int'>` instead of `<class 'numpy.ndarray'>`"""
        self.assertEqual(the_exception.args[0], error_code)
    def test_inc_is_not_int(self):
        # md, inc, and azim can not have negative values, should throw error

        current_dir = Path.cwd()
        path = current_dir.parent / 'data'
        json_path = path / 'wellbore_survey.json'

        with open(json_path) as json_file:
            data = json.load(json_file)
        json_file.close()

        # convert param to int for error
        param_int = 1

        # create directional survey object
        # requires func for test
        def error_func(data, inc_int):
            DirectionalSurvey(wellId=data['wellId'],
                          md=np.array(data['md']),
                          inc=param_int,
                          azim=np.array(data['azim']),
                          surface_latitude=data['surface_latitude'],
                          surface_longitude=data['surface_longitude']
                          )
        # create error raise
        with self.assertRaises(ValueError) as cm:
            error_func(data, param_int)
        the_exception = cm.exception
        #print(the_exception.args[0])
        error_code = "The field `inc` was assigned by `<class 'int'>` instead of `<class 'numpy.ndarray'>`"
        self.assertEqual(the_exception.args[0], error_code)

    def test_azim_is_not_int(self):
        # md, inc, and azim can not have negative values, should throw error

        current_dir = Path.cwd()
        path = current_dir.parent / 'data'
        json_path = path / 'wellbore_survey.json'

        with open(json_path) as json_file:
            data = json.load(json_file)
        json_file.close()

        # convert param to int for error
        param_int = 1

        # create directional survey object
        # requires func for test
        def error_func(data, inc_int):
            DirectionalSurvey(wellId=data['wellId'],
                          md=np.array(data['md']),
                          inc=np.array(data['inc']),
                          azim=param_int,
                          surface_latitude=data['surface_latitude'],
                          surface_longitude=data['surface_longitude']
                          )
        # create error raise
        with self.assertRaises(ValueError) as cm:
            error_func(data, param_int)
        the_exception = cm.exception
        #print(the_exception.args[0])
        error_code = "The field `azim` was assigned by `<class 'int'>` instead of `<class 'numpy.ndarray'>`"
        self.assertEqual(the_exception.args[0], error_code)
# VALUES ARE NOT LISTS:

    def test_md_is_not_list(self):
        # md, inc, and azim can not have negative values, should throw error

        current_dir = Path.cwd()
        path = current_dir.parent / 'data'
        json_path = path / 'wellbore_survey.json'

        with open(json_path) as json_file:
            data = json.load(json_file)
        json_file.close()

        # create directional survey object
        # requires func for test
        def error_func(data):
            DirectionalSurvey(wellId=data['wellId'],
                          md=data['md'],
                          inc=np.array(data['inc']),
                          azim=np.array(data['azim']),
                          surface_latitude=data['surface_latitude'],
                          surface_longitude=data['surface_longitude']
                          )
        # create error raise
        with self.assertRaises(ValueError) as cm:
            error_func(data)
        the_exception = cm.exception
        #print(the_exception.args[0])
        error_code = "The field `md` was assigned by `<class 'list'>` instead of `<class 'numpy.ndarray'>`"
        self.assertEqual(the_exception.args[0], error_code)



    # def test_arrays_are_equal_len(self):
    #     # md, inc, and azim can not have negative values, should throw error
    #
    #     current_dir = Path.cwd()
    #     path = current_dir.parent / 'data'
    #     json_path = path / 'wellbore_survey.json'
    #
    #     with open(json_path) as json_file:
    #         data = json.load(json_file)
    #     json_file.close()
    #
    #     # convert param to int for error
    #     param_array = np.array([10,15,40])
    #
    #     # create directional survey object
    #     # requires func for test
    #     def error_func(data, inc_int):
    #         DirectionalSurvey(wellId=data['wellId'],
    #                       md=np.array(data['md']),
    #                       inc=np.array(data['inc']),
    #                       azim=param_array,
    #                       surface_latitude=data['surface_latitude'],
    #                       surface_longitude=data['surface_longitude']
    #                       )
    #     # create error raise
    #
    #     print()
    #
    #     with self.assertRaises(ValueError) as cm:
    #         error_func(data, param_array)
    #     the_exception = cm.exception
    #     #print(the_exception.args[0])
    #     error_code = "The field `azim` was assigned by `<class 'int'>` instead of `<class 'numpy.ndarray'>`"
    #     self.assertEqual(the_exception.args[0], error_code)
    # def test_param_neg(self):
    #     # md, inc, and azim can not have negative values, should throw error
    #
    #     current_dir = Path.cwd()
    #     path = current_dir.parent / 'data'
    #     json_path = path / 'wellbore_survey.json'
    #
    #     with open(json_path) as json_file:
    #         data = json.load(json_file)
    #     json_file.close()
    #
    #     # convert md to neg values
    #     md_neg = np.multiply(data['md'], -1)
    #     inc_neg = np.multiply(data['inc'], -1)
    #     azim_neg = np.multiply(data['azim'], -1)
    #
    #     # create directional survey object
    #     directional_survey = DirectionalSurvey(wellId=data['wellId'],
    #                                            md=md_neg,
    #                                            inc=inc_neg,
    #                                            azim=azim_neg,
    #                                            surface_latitude=data['surface_latitude'],
    #                                            surface_longitude=data['surface_longitude'],
    #                                            )
    #
    #     survey_obj = Survey(directional_survey)
    #
    #     self.assertEqual(len(survey_obj.directional_survey_points.md), 110, 'incorrect')
#
#     def test_param_max_value(self):
#         # azim can not be above 360, inc can not have values above 100, should throw error
#         # TODO: should I include the inc value?
#         # TODO: should I include a conversion, if azim greater than 360 subtract 360?
#
#         current_dir = Path.cwd()
#         path = current_dir.parent / 'data'
#         json_path = path / 'wellbore_survey.json'
#
#         with open(json_path) as json_file:
#             data = json.load(json_file)
#         json_file.close()
#
#         # convert md to neg values
#         azim_double = np.multiply(data['azim'], 2)
#         inc_double = np.multiply(data['inc'], 2)
#
#         # create directional survey object
#         directional_survey = DirectionalSurvey(wellId=data['wellId'],
#                                                md=data['md'],
#                                                inc=inc_double,
#                                                azim=azim_double,
#                                                surface_latitude=data['surface_latitude'],
#                                                surface_longitude=data['surface_longitude'],
#                                                )
#
#         survey_obj = Survey(directional_survey)
#
#         self.assertEqual(len(survey_obj.directional_survey_points.azim), 110, 'incorrect')
#
#     def test_param_not_array(self):
#         # md, inc, and azim can not have negative values, should throw error
#
#         current_dir = Path.cwd()
#         path = current_dir.parent / 'data'
#         json_path = path / 'wellbore_survey.json'
#
#         with open(json_path) as json_file:
#             data = json.load(json_file)
#         json_file.close()
#
#         # convert md to neg values
#         wellId_list = [data['wellId'] for i in range(110)]
#         #wellId_list = data['wellId']
#
#         # create directional survey object
#         directional_survey = DirectionalSurvey(wellId=wellId_list,
#                                                md=data['md'],
#                                                inc=data['inc'],
#                                                azim=data['azim'],
#                                                surface_latitude=data['surface_latitude'],
#                                                surface_longitude=data['surface_longitude'],
#                                                )
#
#         survey_obj = Survey(directional_survey)
#         print(survey_obj.directional_survey_points)
#
#         # run survey points calc
#         survey_points_obj = survey_obj.calculate_survey_points()
#
#         # convert to df
#         df_min_curve = Survey.get_survey_df(survey_points_obj)
#         print(df_min_curve)
#
#         self.assertEqual(len(survey_obj.directional_survey_points.md), 110, 'incorrect')
#
if __name__ == '__main__':
    unittest.main()
