# from src.directional_survey import *
# import unittest
#
# class TestRead(unittest.TestCase):
#
#     # TYPE ERRORS, md, inc, azim, wellid, surface lat and lon must be present
#     def test_required_data_is_present(self):
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
#         # create directional survey object
#         # requires func for test
#         def error_func():
#             DataObject()
#
#         # create error raise
#         with self.assertRaises(TypeError) as cm:
#             error_func()
#         the_exception = cm.exception
#         #print(the_exception.args[0])
#         error_code = """__init__() missing 6 required positional arguments: 'wellId', 'md', 'inc', 'azim', 'surface_latitude', and 'surface_longitude'"""
#         self.assertEqual(the_exception.args[0], error_code)
#
#
# # VALUES ARE NOT INTS
#     def test_md_is_not_int(self):
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
#         # convert param to int for error
#         param_int = 1
#
#         # create directional survey object
#         # requires func for test
#         def error_func(data, param_int):
#             DataObject(wellId=data['wellId'],
#                        md=param_int,
#                        inc=np.array(data['inc']),
#                        azim=np.array(data['azim']),
#                        surface_latitude=data['surface_latitude'],
#                        surface_longitude=data['surface_longitude']
#                        )
#         # create error raise
#         with self.assertRaises(ValueError) as cm:
#             error_func(data, param_int)
#         the_exception = cm.exception
#         #print(the_exception.args[0])
#         error_code = """The field `md` was assigned by `<class 'int'>` instead of `<class 'numpy.ndarray'>`"""
#         self.assertEqual(the_exception.args[0], error_code)
#     def test_inc_is_not_int(self):
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
#         # convert param to int for error
#         param_int = 1
#
#         # create directional survey object
#         # requires func for test
#         def error_func(data, inc_int):
#             DataObject(wellId=data['wellId'],
#                        md=np.array(data['md']),
#                        inc=param_int,
#                        azim=np.array(data['azim']),
#                        surface_latitude=data['surface_latitude'],
#                        surface_longitude=data['surface_longitude']
#                        )
#         # create error raise
#         with self.assertRaises(ValueError) as cm:
#             error_func(data, param_int)
#         the_exception = cm.exception
#         #print(the_exception.args[0])
#         error_code = "The field `inc` was assigned by `<class 'int'>` instead of `<class 'numpy.ndarray'>`"
#         self.assertEqual(the_exception.args[0], error_code)
#
#     def test_azim_is_not_int(self):
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
#         # convert param to int for error
#         param_int = 1
#
#         # create directional survey object
#         # requires func for test
#         def error_func(data, inc_int):
#             DataObject(wellId=data['wellId'],
#                        md=np.array(data['md']),
#                        inc=np.array(data['inc']),
#                        azim=param_int,
#                        surface_latitude=data['surface_latitude'],
#                        surface_longitude=data['surface_longitude']
#                        )
#         # create error raise
#         with self.assertRaises(ValueError) as cm:
#             error_func(data, param_int)
#         the_exception = cm.exception
#         #print(the_exception.args[0])
#         error_code = "The field `azim` was assigned by `<class 'int'>` instead of `<class 'numpy.ndarray'>`"
#         self.assertEqual(the_exception.args[0], error_code)
# # VALUES ARE NOT LISTS:
#
#     def test_md_is_not_list(self):
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
#         # create directional survey object
#         # requires func for test
#         def error_func(data):
#             DataObject(wellId=data['wellId'],
#                        md=data['md'],
#                        inc=np.array(data['inc']),
#                        azim=np.array(data['azim']),
#                        surface_latitude=data['surface_latitude'],
#                        surface_longitude=data['surface_longitude']
#                        )
#         # create error raise
#         with self.assertRaises(ValueError) as cm:
#             error_func(data)
#         the_exception = cm.exception
#         #print(the_exception.args[0])
#         error_code = "The field `md` was assigned by `<class 'list'>` instead of `<class 'numpy.ndarray'>`"
#         self.assertEqual(the_exception.args[0], error_code)
#
#
#
#     def test_arrays_are_equal_len(self):
#
#             current_dir = Path.cwd()
#             path = current_dir.parent / 'data'
#             json_path = path / 'wellbore_survey.json'
#
#             with open(json_path) as json_file:
#                 data = json.load(json_file)
#             json_file.close()
#
#
#
#             param_val = [1,2,3]
#
#             # create directional survey object
#             # requires func for test
#             def error_func(data, param_val):
#                 DataObject(wellId=data['wellId'],
#                            md=np.array(param_val),
#                            inc=np.array(data['inc']),
#                            azim=np.array(data['azim']),
#                            surface_latitude=data['surface_latitude'],
#                            surface_longitude=data['surface_longitude']
#                            )
#
#             # create error raise
#             with self.assertRaises(ValueError) as cm:
#                 error_func(data, param_val)
#             the_exception = cm.exception
#             #print(the_exception.args[0])
#             error_code = "Validation Error: Array lengths must be equal, md length: `3` md length: `110` md length: `110`"
#             self.assertEqual(the_exception.args[0], error_code)
#
#     def test_md_array_sign(self):
#
#             current_dir = Path.cwd()
#             path = current_dir.parent / 'data'
#             json_path = path / 'wellbore_survey.json'
#
#             with open(json_path) as json_file:
#                 data = json.load(json_file)
#             json_file.close()
#
#             # create directional survey object
#             # requires func for test
#             def error_func(data):
#                 DataObject(wellId=data['wellId'],
#                            md=np.array(data['md'])*-1,
#                            inc=np.array(data['inc']),
#                            azim=np.array(data['azim']),
#                            surface_latitude=data['surface_latitude'],
#                            surface_longitude=data['surface_longitude']
#                            )
#
#             # create error raise
#             with self.assertRaises(ValueError) as cm:
#                 error_func(data)
#             the_exception = cm.exception
#             #print(the_exception.args[0])
#             error_code = "Validation Error: MD array has negative values"
#             self.assertEqual(the_exception.args[0], error_code)
#
#     def test_inc_array_sign(self):
#
#             current_dir = Path.cwd()
#             path = current_dir.parent / 'data'
#             json_path = path / 'wellbore_survey.json'
#
#             with open(json_path) as json_file:
#                 data = json.load(json_file)
#             json_file.close()
#
#             # create directional survey object
#             # requires func for test
#             def error_func(data):
#                 DataObject(wellId=data['wellId'],
#                            md=np.array(data['md']),
#                            inc=np.array(data['inc'])*-1,
#                            azim=np.array(data['azim']),
#                            surface_latitude=data['surface_latitude'],
#                            surface_longitude=data['surface_longitude']
#                            )
#
#             # create error raise
#             with self.assertRaises(ValueError) as cm:
#                 error_func(data)
#             the_exception = cm.exception
#             #print(the_exception.args[0])
#             error_code = "Validation Error: INC array has negative values"
#             self.assertEqual(the_exception.args[0], error_code)
#
#     def test_azim_array_values(self):
#
#             current_dir = Path.cwd()
#             path = current_dir.parent / 'data'
#             json_path = path / 'wellbore_survey.json'
#
#             with open(json_path) as json_file:
#                 data = json.load(json_file)
#             json_file.close()
#
#             # create directional survey object
#             # requires func for test
#             def error_func(data):
#                 DataObject(wellId=data['wellId'],
#                            md=np.array(data['md']),
#                            inc=np.array(data['inc']),
#                            azim=np.array(data['azim'])*10,
#                            surface_latitude=data['surface_latitude'],
#                            surface_longitude=data['surface_longitude']
#                            )
#
#             # create error raise
#             with self.assertRaises(ValueError) as cm:
#                 error_func(data)
#             the_exception = cm.exception
#             #print(the_exception.args[0])
#             error_code = "Validation Error: AZIM array must have values between 0 and 360"
#             self.assertEqual(the_exception.args[0], error_code)
# #
# if __name__ == '__main__':
#     unittest.main()
