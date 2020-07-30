import unittest
from src.transforms import *
from src.wellbore_trajectory import *

# Unit tests
# TODO find out how to move this to the tests folder, having trouble with paths

class TestLatLonCalc(unittest.TestCase):

    def test_lat_lon_calc(self):
        current_dir = Path.cwd()
        path = current_dir.parent

        # get wellbore df
        file = path / 'data/wellbore_survey.csv'
        df = pd.read_csv(file, sep=',')
        df_lat_lon_orig = df[['latitude_decimal_deg', 'longitude_decimal_deg']]

        #get wellbore json

        file_path = get_files(path, folders='data', extensions='.json')
        file_path = file_path.items[0]

        # with open(json_path[0]) as json_file:
        #     data = json.load(json_file)
        # json_file.close()
        #print(file_path)

        # get survey obj
        well_obj = WellboreTrajectory.from_json(file_path)
        #well_obj = WellboreTrajectory(data)

        # calculate survey points
        well_obj.calculate_survey_points()

        # convert to df
        df_min_curve = well_obj.get_survey_df()

        # merge original df (with official lat lon points) and calculated lat lon points
        df_test = pd.merge(df_min_curve, df_lat_lon_orig, left_index=True, right_index=True)

        def get_change(current, previous):
            # get abs change, else 0
            if current == previous:
                return 0
            try:
                return (abs(current - previous) / previous) * 100.0
            except ZeroDivisionError:
                return float('inf')

        # lat test
        lat_test_list = list(zip(df_test['latitude_points'], df_test['latitude_decimal_deg']))
        # get abs change
        max_lat_delta = max([get_change(row[0], row[1]) for row in lat_test_list])

        # lon test
        lon_test_list = list(zip(df_test['longitude_points'], df_test['longitude_decimal_deg']))
        # get abs change
        max_lon_delta = max([get_change(row[0], row[1]) for row in lon_test_list])

        # tolerance test
        # if the highest delta from the actual lat or lon points is less than 0.01% the survey passes
        self.assertEqual(round(max_lat_delta * 10000), 0, 'latitude calculation not within 0.001%')
        self.assertEqual(round(max_lon_delta * 10000), 0, 'longitude calculation not within 0.001%')


if __name__ == '__main__':
    unittest.main()
