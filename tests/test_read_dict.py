import unittest
from src.directional_survey import *


class TestReadDict(unittest.TestCase):

    def test_read_dict(self):
        path = Path().resolve().parent
        json_path = path / 'data/wellbore_survey_v2.json'

        with open(json_path) as json_file:
            data = json.load(json_file)
        json_file.close()

        survey_obj = Survey(data)
        #print(survey_obj.directional_survey_points.wellId)
        #print(survey_obj.directional_survey_points.surface_longitude)

        #print(sum(survey_obj.directional_survey_points.surface_latitude))

        self.assertEqual(len(survey_obj.directional_survey_points.wellId), 110, 'incorrect')
        self.assertEqual(len(survey_obj.directional_survey_points.md), 110, 'incorrect')
        self.assertEqual(len(survey_obj.directional_survey_points.inc), 110, 'incorrect')
        self.assertEqual(len(survey_obj.directional_survey_points.azim), 110, 'incorrect')
        self.assertEqual(len(survey_obj.directional_survey_points.surface_latitude), 110, 'incorrect')
        self.assertEqual(len(survey_obj.directional_survey_points.surface_longitude), 110, 'incorrect')


if __name__ == '__main__':
    unittest.main()
