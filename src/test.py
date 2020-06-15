# Any changes to the distributions library should be reinstalled with
#  pip install --upgrade .

# For running unit tests, use
# /usr/bin/python -m unittest test

import unittest
#from pathlib import Path
#from src.dataclass import *
#from src.directional_survey import *
#path = Path().resolve().parent
#path = path/'src'
#print(path)
from dataclass import *
from directional_survey import *

# Unit tests
# TODO find out how to move this to the tests folder, having trouble with paths
import unittest

class TestMinCurve(unittest.TestCase):
    
    def test_survey_obj_data(self):
        
        path = Path().resolve().parent
        file = path/'data/wellbore_survey_3.csv'

        df = pd.read_csv(file, sep=',')

        df = df[['wellId','md','inc','azim','surface_latitude','surface_longitude']]
        
        survey_dict = df.to_dict(orient='records')
        survey_obj = Survey(survey_dict)
        self.assertEqual(len(survey_obj.directional_survey_points.wellId),110,'incorrect')
        self.assertEqual(len(survey_obj.directional_survey_points.md),110,'incorrect')
        self.assertEqual(len(survey_obj.directional_survey_points.inc),110,'incorrect')
        self.assertEqual(len(survey_obj.directional_survey_points.azim),110,'incorrect')
        self.assertEqual(len(survey_obj.directional_survey_points.surface_latitude),110,'incorrect')
        self.assertEqual(len(survey_obj.directional_survey_points.surface_longitude),110,'incorrect')
        

    def test_lat_long_calculation(self):
        
        path = Path().resolve().parent
        file = path/'data/wellbore_survey_3.csv'

        df = pd.read_csv(file, sep=',')
        
        df_latlon_orig = df[['latitude_decimal_deg','longitude_decimal_deg']]
        df = df[['wellId','md','inc','azim','surface_latitude','surface_longitude']]
        survey_dict = df.to_dict(orient='records')
        
        # get survey obj
        survey_obj = Survey(survey_dict)
        
        # run min curve algo
        df_min_curve = survey_obj.minimum_curvature_algo()

        df_test = pd.merge(df_min_curve,df_latlon_orig,left_index=True,right_index=True)

        def get_change(current, previous):
            # get abs change, else 0
            if current == previous:
                return 0
            try:
                return (abs(current - previous) / previous) * 100.0
            except ZeroDivisionError:
                return float('inf')

        #lat test
        lat_test_list = list(zip(df_test['latitude_points'], df_test['latitude_decimal_deg']))
        # get abs change
        max_lat_delta = max([get_change(row[0],row[1]) for row in lat_test_list])
        
        #lon test
        lon_test_list = list(zip(df_test['longitude_points'], df_test['longitude_decimal_deg']))
        # get abs change
        max_lon_delta = max([get_change(row[0],row[1]) for row in lon_test_list])
        
        # tolerance test
        # if the highest delta from the actual lat or lon points is less than 0.01% the survey passes
        self.assertEqual(round(max_lat_delta*10000),0,'latitude calculation not within 0.001%')    
        self.assertEqual(round(max_lon_delta*10000),0,'longitude calculation not within 0.001%')
        
        
# tests = TestMinCurve()

# tests_loaded = unittest.TestLoader().loadTestsFromModule(tests)

# unittest.TextTestRunner().run(tests_loaded)

if __name__ == '__main__':
    unittest.main()