import unittest
from src.utils import *
from src.wellbore_trajectory import *


class TestSurfaceLatLongVSXY(unittest.TestCase):

    def test_surface_lat_long_vs_x_y(self):
        current_dir = Path.cwd()
        path = current_dir.parent
        # Get data that only has x and y surface locations, calculate survey points for comparison
        # get data that has only surface x and y, wellid, md, inc, azim
        json_path = path / 'tests/bench/well_export.json'
        with open(json_path) as json_file:
            json_obj = json.load(json_file)
        json_file.close()
        # create a dict that has only the surface x and y
        well_dict = {'wellId': json_obj['wellId'],
                     'md': json_obj['md'],
                     'inc': json_obj['inc'],
                     'azim': json_obj['azim'],
                     'surface_x': json_obj['surface_x'],
                     'surface_y': json_obj['surface_y']}

        well_obj = WellboreTrajectory(data=well_dict)

        # must import crs transform string
        well_obj.crs_transform(crs_in='epsg:32638')
        well_obj.calculate_survey_points()
        json_ds = well_obj.serialize()

        json_ds_obj = json.loads(json_ds)
        # convert to df and keep only the lat and long points
        dfXY = pd.DataFrame(json_ds_obj)
        dfXY = dfXY[['longitude_points', 'latitude_points']]

        # calculate survey points from json with surface lat and long
        file_path = path / 'data/wellbore_survey.json'
        well_obj = WellboreTrajectory.from_json(file_path)

        # calculate survey points
        well_obj.calculate_survey_points()

        # serialize data object
        json_ds = well_obj.serialize()

        # load and convert to df
        json_ds_obj = json.loads(json_ds)
        df_min_curve = pd.DataFrame(json_ds_obj)

        # merge original df (with official lat lon points) and calculated lat lon points
        df_test = pd.merge(df_min_curve, dfXY, left_index=True, right_index=True)

        def get_change(current, previous):
            # get abs change, else 0
            if current == previous:
                return 0
            try:
                return (abs(current - previous) / previous) * 100.0
            except ZeroDivisionError:
                return float('inf')

        # lat test
        lat_test_list = list(zip(df_test['latitude_points_x'], df_test['latitude_points_y']))
        # get abs change
        max_lat_delta = max([get_change(row[0], row[1]) for row in lat_test_list])

        # lon test
        lon_test_list = list(zip(df_test['longitude_points_x'], df_test['longitude_points_y']))
        # get abs change
        max_lon_delta = max([get_change(row[0], row[1]) for row in lon_test_list])

        # tolerance test
        # if the highest delta from the actual lat or lon points is less than 0.01% the survey passes
        self.assertEqual(round(max_lat_delta * 10000), 0, 'latitude calculation not within 0.001%')
        self.assertEqual(round(max_lon_delta * 10000), 0, 'longitude calculation not within 0.001%')


if __name__ == '__main__':
    unittest.main()
