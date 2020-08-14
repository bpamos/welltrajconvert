import unittest
from src.wellbore_trajectory import *


class TestLatLonJsonVSBenchmark(unittest.TestCase):

    def test_lat_lon_json_vs_benchmark(self):
        current_dir = Path.cwd()
        path = current_dir.parent

        # load correct json file export for comparision
        json_path = path / 'tests/bench/well_export.json'
        with open(json_path) as json_file:
            json_export = json.load(json_file)
        json_file.close()

        # get survey obj
        file_path = path/'data/wellbore_survey.json'
        well_obj = WellboreTrajectory.from_json(file_path)

        # calculate survey points
        well_obj.calculate_survey_points()

        # deserialize data object
        json_ds = well_obj.deserialize()

        #load json string
        json_ds = json.loads(json_ds)

        self.assertEqual(json_ds['wellId'] == json_export['wellId'], True, 'wellId strings are not equal')
        self.assertEqual(json_ds['md'] == json_export['md'], True, 'md lists are not equal')
        self.assertEqual(json_ds['inc'] == json_export['inc'], True, 'inc lists are not equal')
        self.assertEqual(json_ds['azim'] == json_export['azim'], True, 'azim lists are not equal')
        self.assertEqual(json_ds['e_w_deviation'] == json_export['e_w_deviation'], True,
                         'e_w_deviation lists are not equal')
        self.assertEqual(json_ds['n_s_deviation'] == json_export['n_s_deviation'], True,
                         'n_s_deviation lists are not equal')
        self.assertEqual(json_ds['dls'] == json_export['dls'], True,
                         'dls lists are not equal')
        self.assertEqual(json_ds['surface_latitude'] == json_export['surface_latitude'], True,
                         'surface_latitude floats are not equal')
        self.assertEqual(json_ds['surface_longitude'] == json_export['surface_longitude'],
                         True, 'surface_longitude floats are not equal')
        self.assertEqual(json_ds['longitude_points'] == json_export['longitude_points'],
                         True, 'longitude_points lists are not equal')
        self.assertEqual(json_ds['latitude_points'] == json_export['latitude_points'],
                         True, 'latitude_points lists are not equal')
        self.assertEqual(json_ds['zone_number'] == json_export['zone_number'], True,
                         'zone_number ints are not equal')
        self.assertEqual(json_ds['zone_letter'] == json_export['zone_letter'], True,
                         'zone_letter strings are not equal')
        self.assertEqual(json_ds['x_points'] == json_export['x_points'], True,
                         'x_points lists are not equal')
        self.assertEqual(json_ds['y_points'] == json_export['y_points'], True,
                         'y_points lists are not equal')
        self.assertEqual(json_ds['surface_x'] == json_export['surface_x'], True,
                         'surface_x floats are not equal')
        self.assertEqual(json_ds['surface_y'] == json_export['surface_y'], True,
                         'surface_y floats are not equal')
        self.assertEqual(json_ds['isHorizontal'] == json_export['isHorizontal'], True,
                         'isHorizontal lists are not equal')
        json_comp = sorted(json_ds.items()) == sorted(json_export.items())
        self.assertEqual(json_comp, True, 'Json objects are not equal')




if __name__ == '__main__':
    unittest.main()