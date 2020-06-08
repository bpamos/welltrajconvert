
import pandas as pd
from src.utils import *
from src.dataclass import *

class Survey:
    """
    Get information about a directional survey from json files
    reformat into directional survey obj
    """

    def __init__(self, directional_survey_data):
        """
        Survey object with a wells directional survey info

        Attributes:
        directional_survey_points (Dataclass Object) DirectionalSurvey object
        """
        directional_survey_points = get_directional_survey_dataclass(directional_survey_data)

        self.directional_survey_points = directional_survey_points

    
    def calculate_xy_offsets(self):
        """
        convert n/s and e/w deviations and their n/s, e/w ids to x and y offsets
        and replace the original data with new updated directional survey points
        """
        df = pd.DataFrame({'e_w_deviation':self.directional_survey_points.e_w_deviation,
                         'e_w':self.directional_survey_points.e_w,
                         'n_s_deviation':self.directional_survey_points.n_s_deviation,
                         'n_s':self.directional_survey_points.n_s})

        df['e_w'] = df['e_w'].str.lower()
        df['n_s'] = df['n_s'].str.lower()

        #X_OFFSET is equal to e_w_deviation when E is positive and W is negative
        #Y_OFFSET is equal to n_s_deviation when N is positive and S is negative
            
        # create dict to map for offset
        offsetDict = {
            "e" : 1,
            "w" : -1,
            "n" : 1,
            "s" : -1
        }
        # create new columns and map dict * the deviations
        df['x_offset']= df['e_w'].map(offsetDict)*df['e_w_deviation']
        df['y_offset']= df['n_s'].map(offsetDict)*df['n_s_deviation']

        #offset_dict = df.to_dict(orient='records')

        #directional_survey_points = get_directional_survey_dataclass(offset_dict)
        #self.directional_survey_points = directional_survey_points

        #return self.directional_survey_points
        return df

        
    def get_utm_points(self):


        df = pd.DataFrame({'surface_latitude':self.directional_survey_points.surface_latitude,
                    'surface_longitude':self.directional_survey_points.surface_longitude })


        df[['surface_x','surface_y','zone_number','zone_letter']] = df[['surface_latitude','surface_longitude']].apply(get_utms , axis=1)
        
        print('converted surface x and y to surface lat and long')

        return df

    def get_xy_points(self):

        df = pd.DataFrame({'surface_x':self.directional_survey_points.surface_x,
                        'surface_y':self.directional_survey_points.surface_y,
                        'x_offset':self.directional_survey_points.x_offset,
                        'y_offset':self.directional_survey_points.y_offset, })

            # create X and Y columns for each deviation point per uwi
        # add the x and y offset to the surface x and y for each uwi
        df['x_points'] = df['surface_x']+(df['x_offset']*0.3048)
        df['y_points'] = df['surface_y']+(df['y_offset']*0.3048)

        return df


    def get_lat_lon_points(self):

        df = pd.DataFrame({'x_points':self.directional_survey_points.x_points,
                    'y_points':self.directional_survey_points.y_points,
                    'zone_number':self.directional_survey_points.zone_number,
                    'zone_letter':self.directional_survey_points.zone_letter })

        # convert adjusted x and y back to lat long
        df[['latitude_points','longitude_points']] = df[['x_points','y_points','zone_number','zone_letter']].apply(get_latlon , axis=1)
        print('converted adjusted x and y back to lat long')

        return df  
