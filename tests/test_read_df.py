# from src.directional_survey import *
#
# # Unit tests
# # TODO remove this test, removing running off of dfs and converting to run off dict
# import unittest
#
#
# class TestReadDf(unittest.TestCase):
#
#     def test_read_df(self):
#
#         path = Path().resolve().parent
#         file = path / 'data/wellbore_survey_3.csv'
#
#         df = pd.read_csv(file, sep=',')
#
#         df = df[['wellId', 'md', 'inc', 'azim', 'surface_latitude', 'surface_longitude']]
#
#         survey_dict = df.to_dict(orient='records')
#         survey_obj = Survey(survey_dict)
#         self.assertEqual(len(survey_obj.directional_survey_points.wellId), 110, 'incorrect')
#         self.assertEqual(len(survey_obj.directional_survey_points.md), 110, 'incorrect')
#         self.assertEqual(len(survey_obj.directional_survey_points.inc), 110, 'incorrect')
#         self.assertEqual(len(survey_obj.directional_survey_points.azim), 110, 'incorrect')
#         self.assertEqual(len(survey_obj.directional_survey_points.surface_latitude), 110, 'incorrect')
#         self.assertEqual(len(survey_obj.directional_survey_points.surface_longitude), 110, 'incorrect')
#
#
# if __name__ == '__main__':
#     unittest.main()
