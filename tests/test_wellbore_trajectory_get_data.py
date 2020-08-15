import unittest
from src.wellbore_trajectory import *


def compare_arrays(array_a, array_b):
    """compare array a and array b values"""
    comparison = array_a == np.array(array_b)
    return comparison.all()

class TestWellboreTrajectoryGetData(unittest.TestCase):

    def test_wellbore_trajectory_get_data(self):
        well_dict = {
            "wellId": "well_A",
            "md": [5000.0, 5200.0, 5400.0, 5600.55, 5800.0, 5900.0],
            "inc": [70.97, 75.88, 80.15, 85.03, 89.91, 90.97],
            "azim": [28.78, 28.53, 29.28, 27.59, 26.69, 26.72],
            "surface_latitude": 29.90829444,
            "surface_longitude": 47.68852083
        }
        # get wellbore trajectory object
        dev_obj = WellboreTrajectory(well_dict)

        self.assertEqual(dev_obj.deviation_survey_obj.wellId, 'well_A', 'incorrect well name value')
        array_a = dev_obj.deviation_survey_obj.md
        array_b = [5000.0, 5200.0, 5400.0, 5600.55, 5800.0, 5900.0]
        self.assertEqual(compare_arrays(array_a, array_b), True, 'md arrays are not equal')
        array_a = dev_obj.deviation_survey_obj.inc
        array_b = [70.97, 75.88, 80.15, 85.03, 89.91, 90.97]
        self.assertEqual(compare_arrays(array_a, array_b), True, 'inc arrays are not equal')
        array_a = dev_obj.deviation_survey_obj.azim
        array_b = [28.78, 28.53, 29.28, 27.59, 26.69, 26.72]
        self.assertEqual(compare_arrays(array_a, array_b), True, 'azim arrays are not equal')
        self.assertEqual(dev_obj.deviation_survey_obj.surface_latitude, 29.90829444, 'incorrect surface lat value')
        self.assertEqual(dev_obj.deviation_survey_obj.surface_longitude, 47.68852083, 'incorrect surface lon value')


if __name__ == '__main__':
    unittest.main()
