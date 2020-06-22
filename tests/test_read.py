import unittest
from src.directional_survey import *

class TestRead(unittest.TestCase):
    def test_param_neg(self):
        # md, inc, and azim can not have negative values, should throw error

        current_dir = Path.cwd()
        path = current_dir.parent / 'data'
        json_path = path / 'wellbore_survey_v3.json'

        with open(json_path) as json_file:
            data = json.load(json_file)
        json_file.close()

        # convert md to neg values
        md_neg = np.multiply(data['md'], -1)
        inc_neg = np.multiply(data['inc'], -1)
        azim_neg = np.multiply(data['azim'], -1)

        # create directional survey object
        directional_survey = DirectionalSurvey(wellId=data['wellId'],
                                               md=md_neg,
                                               inc=inc_neg,
                                               azim=azim_neg,
                                               surface_latitude=data['surface_latitude'],
                                               surface_longitude=data['surface_longitude'],
                                               )

        survey_obj = Survey(directional_survey)

        self.assertEqual(len(survey_obj.directional_survey_points.md), 110, 'incorrect')

    def test_param_max_value(self):
        # azim can not be above 360, inc can not have values above 100, should throw error
        # TODO: should I include the inc value?
        # TODO: should I include a conversion, if azim greater than 360 subtract 360?

        current_dir = Path.cwd()
        path = current_dir.parent / 'data'
        json_path = path / 'wellbore_survey_v3.json'

        with open(json_path) as json_file:
            data = json.load(json_file)
        json_file.close()

        # convert md to neg values
        azim_double = np.multiply(data['azim'], 2)
        inc_double = np.multiply(data['inc'], 2)

        # create directional survey object
        directional_survey = DirectionalSurvey(wellId=data['wellId'],
                                               md=data['md'],
                                               inc=inc_double,
                                               azim=azim_double,
                                               surface_latitude=data['surface_latitude'],
                                               surface_longitude=data['surface_longitude'],
                                               )

        survey_obj = Survey(directional_survey)

        self.assertEqual(len(survey_obj.directional_survey_points.azim), 110, 'incorrect')

if __name__ == '__main__':
    unittest.main()
