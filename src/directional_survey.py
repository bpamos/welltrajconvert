
import pandas as pd
from src.utils import *
from src.dataclass import *

class Survey:
    """
    Get information about a directional survey from dict
    reformat into directional survey obj
    """

    def __init__(self, directional_survey_data):
        """
        Survey object with a wells directional survey info

        Attributes:
        directional_survey_points (Dataclass Object) DirectionalSurvey object
        """
        #convert survey data into its dataclass obj
        directional_survey_points = get_directional_survey_dataclass(directional_survey_data)

        self.directional_survey_points = directional_survey_points

    
    def calculate_xy_offsets(self):
        """
        convert n/s and e/w deviations and their n/s, e/w ids to x and y offsets
        and replace the original data with new updated directional survey points

        Args:
        None
        
        required data:
        e_w_deviation
        e_w
        n_s_deviation
        n_s

        Returns:
        df with xy offset
        """
        if self.directional_survey_points.e_w is None and self.directional_survey_points.n_s is None:
            df = pd.DataFrame({'e_w_deviation':self.directional_survey_points.e_w_deviation,
                        'n_s_deviation':self.directional_survey_points.n_s_deviation})
            # create new columns and map dict * the deviations
            df['x_offset']= df['e_w_deviation']
            df['y_offset']= df['n_s_deviation']
            
        else:
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
        """
        get utm points from survey data,
        using the 'get_utms' func translate surface lat and lon into its utm points

        Args:
        None
        
        required data:
        surface_latitude
        surface_longitude

        Returns:
        df with surface x, y, zone number and zone letter
        """

        df = pd.DataFrame({'surface_latitude':self.directional_survey_points.surface_latitude,
                    'surface_longitude':self.directional_survey_points.surface_longitude })


        df[['surface_x','surface_y','zone_number','zone_letter']] = df[['surface_latitude','surface_longitude']].apply(get_utms , axis=1)
        
        print('converted surface x and y to surface lat and long')

        return df

    def get_xy_points(self):
        """
        get x y points from survey data,
        typically this data is not provided and is calculated from 'calculate_xy_offsets' and 'get_utm_points'

        Args:
        None
        
        required data:
        surface_x
        surface_y
        x_offset
        y_offset

        Returns:
        df with x y points
        """

        df = pd.DataFrame({'surface_x':self.directional_survey_points.surface_x,
                        'surface_y':self.directional_survey_points.surface_y,
                        'x_offset':self.directional_survey_points.x_offset,
                        'y_offset':self.directional_survey_points.y_offset, })

        # create X and Y columns for each deviation point
        # add the x and y offset from the surface x and y for each point * meters conversion
        # TODO add meters or feet conversion. Currenlty assumes offset feet and converts to meters
        df['x_points'] = df['surface_x']+(df['x_offset']*0.3048)
        df['y_points'] = df['surface_y']+(df['y_offset']*0.3048)

        return df


    def get_lat_lon_points(self):
        """
        get lat lon points from survey data,
        typically this data is not provided and is calculated from 'get_xy_points' and 'get_utm_points'

        Args:
        None
        
        required data:
        x_points
        y_points
        zone_number
        zone_letter

        Returns:
        df with lat lon points
        """

        df = pd.DataFrame({'x_points':self.directional_survey_points.x_points,
                    'y_points':self.directional_survey_points.y_points,
                    'zone_number':self.directional_survey_points.zone_number,
                    'zone_letter':self.directional_survey_points.zone_letter })

        # convert adjusted x and y back to lat long
        df[['latitude_points','longitude_points']] = df[['x_points','y_points','zone_number','zone_letter']].apply(get_latlon , axis=1)
        print('converted adjusted x and y back to lat long')

        return df

    def get_lat_lon_from_deviation(self):
        """
        get lat lon points from survey if ns and ew deviations and their ew and ns ids are provided.

        Args:
        None
        
        required survey data:
        wellId
        md
        inc
        azim
        e_w_deviation
        e_w
        n_s_deviation
        n_s
        surface_latitude
        surface_longitude

        Returns:
        df with lat lon points and other calculated attributes
        """
        if self.directional_survey_points.e_w is None and self.directional_survey_points.n_s is None:
            survey_df = pd.DataFrame({'wellId':self.directional_survey_points.wellId,
                        'md':self.directional_survey_points.md,
                        'inc':self.directional_survey_points.inc,
                        'azim':self.directional_survey_points.azim,
                        'e_w_deviation':self.directional_survey_points.e_w_deviation,
                        'n_s_deviation':self.directional_survey_points.n_s_deviation,
                        'surface_latitude':self.directional_survey_points.surface_latitude,
                        'surface_longitude':self.directional_survey_points.surface_longitude })
        else:
            survey_df = pd.DataFrame({'wellId':self.directional_survey_points.wellId,
                                    'md':self.directional_survey_points.md,
                                    'inc':self.directional_survey_points.inc,
                                    'azim':self.directional_survey_points.azim,
                                    'e_w_deviation':self.directional_survey_points.e_w_deviation,
                                    'e_w':self.directional_survey_points.e_w,
                                    'n_s_deviation':self.directional_survey_points.n_s_deviation,
                                    'n_s':self.directional_survey_points.n_s,
                                    'surface_latitude':self.directional_survey_points.surface_latitude,
                                    'surface_longitude':self.directional_survey_points.surface_longitude })

        survey_dict = survey_df.to_dict(orient='records')
        survey_obj = Survey(survey_dict)

        offset = survey_obj.calculate_xy_offsets()
        offset = offset[['x_offset','y_offset']]

        utms = survey_obj.get_utm_points()
        utms = utms[['surface_x','surface_y','zone_number','zone_letter']]
        
        
        survey_df = pd.merge(survey_df,offset,left_index=True,right_index=True)
        survey_df = pd.merge(survey_df,utms,left_index=True,right_index=True)

        survey_dict = survey_df.to_dict(orient='records')
        survey_obj = Survey(survey_dict)

        xy_points = survey_obj.get_xy_points()
        xy_points = xy_points[['x_points','y_points']]

        survey_df = pd.merge(survey_df,xy_points,left_index=True,right_index=True)

        survey_dict = survey_df.to_dict(orient='records')
        survey_obj = Survey(survey_dict)

        lat_lon_points = survey_obj.get_lat_lon_points()
        lat_lon_points = lat_lon_points[['latitude_points','longitude_points']]

        survey_df = pd.merge(survey_df,lat_lon_points,left_index=True,right_index=True)

        return survey_df



    def minimum_curvature_algo(self):
        #Following are the calculations for Minimum Curvature Method 


        survey_df = pd.DataFrame({'wellId':self.directional_survey_points.wellId,
                        'md':self.directional_survey_points.md,
                        'inc':self.directional_survey_points.inc,
                        'azim':self.directional_survey_points.azim,
                        'surface_latitude':self.directional_survey_points.surface_latitude,
                        'surface_longitude':self.directional_survey_points.surface_longitude })


        #Convert to Radians

        df = survey_df.reset_index()

        df['inc_rad'] = df['inc']*0.0174533 #converting to radians
        df['azim_rad'] =df['azim']*0.0174533 #converting to radians

        # ************************************************ BETA CALC 
        df['beta'] = np.arccos(
                    np.cos((df['inc_rad']) - (df['inc_rad'].shift(1))) - \
                    (np.sin(df['inc_rad'].shift(1)) * np.sin(df['inc_rad']) * \
                    (1-np.cos(df['azim_rad'] - df['azim_rad'].shift(1)))))

        df['beta'] = df['beta'].fillna(0)

        # *************************************************BETA CALC END

        #DogLeg Severity per 100 ft

        df['dls_sub'] = (df['beta'] * 57.2958 * 100)/(df['md']-df['md'].shift(1))

        # Calc RF
        df['RF'] = np.where(df['beta']==0, 1, 2/df['beta'] * np.tan(df['beta']/2))


        # ************************************************************** TVD CALC

        df['tvd_sub'] = ((df['md']-df['md'].shift(1))/2) * \
                        (np.cos(df['inc_rad'].shift(1)) + np.cos(df['inc_rad']))*df['RF']

        df['tvd_sub'] = df['tvd_sub'].fillna(0)
        df['tvd_sub_cum'] =  df['tvd_sub'].cumsum()

        ### calculating NS
        df['ns_sub'] = ((df['md']-df['md'].shift(1))/2) * \
                        (
                        np.sin(df['inc_rad'].shift(1)) * np.cos(df['azim_rad'].shift(1)) +
                        np.sin(df['inc_rad']) * np.cos(df['azim_rad'])\
                        ) * df['RF']

        df['ns_sub'] = df['ns_sub'].fillna(0)
        df['ns_sub_cum'] =  df['ns_sub'].cumsum()

        ## calculating EW
        df['ew_sub'] = ((df['md']-df['md'].shift(1))/2) * \
                        (
                        np.sin(df['inc_rad'].shift(1)) * \
                        np.sin(df['azim_rad'].shift(1)) + \
                        np.sin(df['inc_rad']) * np.sin(df['azim_rad'])\
                        ) * df['RF']
        df['ew_sub'] = df['ew_sub'].fillna(0)
        df['ew_sub_cum'] =  df['ew_sub'].cumsum()

        df['e_w_deviation'] = df['ew_sub_cum']
        df['n_s_deviation'] = df['ns_sub_cum']


        survey_dict = df.to_dict(orient='records')
        survey_obj = Survey(survey_dict)

        df = survey_obj.get_lat_lon_from_deviation()

        return df