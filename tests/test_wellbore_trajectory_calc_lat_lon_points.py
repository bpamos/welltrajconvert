import unittest
from welltrajconvert.wellbore_trajectory import *


def compare_arrays(array_a, array_b):
    """compare array a and array b values"""
    comparison = array_a == np.array(array_b)
    return comparison.all()

class TestWellboreTrajectoryCalcLatLonPoints(unittest.TestCase):

    def test_wellbore_trajectory_calc_lat_lon_points(self):
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
        dev_obj.minimum_curvature_algorithm()
        dev_obj.calculate_lat_lon_from_deviation_points()

        #TODO: could I have just exported as json and compared
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
        array_a = dev_obj.deviation_survey_obj.tvd.round(3)
        array_b = [0.,  57.036,  98.558, 124.414, 133.216, 132.448]
        self.assertEqual(compare_arrays(array_a, array_b), True, 'tvd arrays are not equal')
        array_a = dev_obj.deviation_survey_obj.n_s_deviation.round(3)
        array_b = [0., 168.163, 339.382, 514.199, 691.458, 780.787]
        self.assertEqual(compare_arrays(array_a, array_b), True, 'n_s_deviation arrays are not equal')
        array_a = dev_obj.deviation_survey_obj.e_w_deviation.round(3)
        array_b = [0.,  91.889, 186.438, 281.081, 371.942, 416.879]
        self.assertEqual(compare_arrays(array_a, array_b), True, 'dls arrays are not equal')
        array_a = dev_obj.deviation_survey_obj.dls.round(3)
        array_b = [0., 2.455, 2.133, 2.421, 2.443, 1.06]
        self.assertEqual(compare_arrays(array_a, array_b), True, 'x_points arrays are not equal')
        array_a = dev_obj.deviation_survey_obj.x_points.round(3)
        array_b = [759587.934, 759615.942, 759644.761, 759673.608, 759701.302, 759714.999]
        self.assertEqual(compare_arrays(array_a, array_b), True, 'y_points arrays are not equal')
        array_a = dev_obj.deviation_survey_obj.y_points.round(3)
        array_b = [3311661.865, 3311713.121, 3311765.309, 3311818.593, 3311872.621, 3311899.849]
        self.assertEqual(compare_arrays(array_a, array_b), True, 'latitude_points arrays are not equal')
        array_a = dev_obj.deviation_survey_obj.latitude_points.round(3)
        array_b = [29.908, 29.909, 29.909, 29.91 , 29.91 , 29.91 ]
        self.assertEqual(compare_arrays(array_a, array_b), True, 'longitude_points arrays are not equal')
        array_a = dev_obj.deviation_survey_obj.longitude_points.round(3)
        array_b = [47.689, 47.689, 47.689, 47.689, 47.69, 47.69]
        self.assertEqual(compare_arrays(array_a, array_b), True, 'e_w_deviation arrays are not equal')
        self.assertEqual(dev_obj.deviation_survey_obj.zone_number, 38, 'incorrect zone_number value')
        self.assertEqual(dev_obj.deviation_survey_obj.zone_letter, 'R', 'incorrect zone_letter value')
        self.assertEqual(dev_obj.deviation_survey_obj.surface_x, 759587.9344401711, 'incorrect surface_x value')
        self.assertEqual(dev_obj.deviation_survey_obj.surface_y, 3311661.864849136, 'incorrect surface_y value')





if __name__ == '__main__':
    unittest.main()