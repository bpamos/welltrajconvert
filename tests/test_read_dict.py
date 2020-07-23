# from src.directional_survey import *
# import unittest
#
# class TestReadDict(unittest.TestCase):
#
#     def test_read_dict(self):
#         current_dir = Path.cwd()
#         path = current_dir.parent / 'data'
#         json_path = path / 'wellbore_survey.json'
#
#         with open(json_path) as json_file:
#             data = json.load(json_file)
#         json_file.close()
#
#         #survey_obj = DirectionalSurvey(data)
#         # TODO: find way to not have to classify things as np.arrays
#         dataclass_obj = DataObject(wellId = data['wellId'],
#                                    md = np.array(data['md']),
#                                    inc = np.array(data['inc']),
#                                    azim = np.array(data['azim']),
#                                    surface_latitude = data['surface_latitude'],
#                                    surface_longitude = data['surface_longitude'])
#         survey_obj = DirectionalSurvey(dataclass_obj)
#
#         self.assertEqual(len([survey_obj.directional_survey_points.wellId]), 1, 'incorrect')
#         self.assertEqual(len(survey_obj.directional_survey_points.md), 110, 'incorrect')
#         self.assertEqual(len(survey_obj.directional_survey_points.inc), 110, 'incorrect')
#         self.assertEqual(len(survey_obj.directional_survey_points.azim), 110, 'incorrect')
#         self.assertEqual(len([survey_obj.directional_survey_points.surface_latitude]), 1, 'incorrect')
#         self.assertEqual(len([survey_obj.directional_survey_points.surface_longitude]), 1, 'incorrect')
#
#
# if __name__ == '__main__':
#     unittest.main()
