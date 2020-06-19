import pandas as pd
import utm
from pathlib import Path
from src.dataclass import *
from src.directional_survey import *

#from dataclass import *
#from directional_survey import *

def get_directional_survey_dataclass(survey_data_list):
    """
    iterates over a list of production data
    looks for field names that match the ProductionMonthly dataclass fields
    converts these key value pairs to np.arrays and puts them in an empty dict
    returns the ProductionMonthly dataclass object for this new dict

    Args:
    survey_data_list (list of dicts) list of directional survey data dicts to iterate over
    (data dict should should match required dict format for DirectionalSurvey dataclass)

    Returns:
    DirectionalSurvey dataclass object for one well
    """

    # DirectionalSurvey dataclass fields
    survey_fields_list = ['wellId', 'md', 'inc', 'azim', 'tvd',
                              'n_s_deviation', 'n_s', 'x_offset', 
                              'e_w_deviation', 'e_w', 'y_offset', 'dls',
                              'surface_latitude', 'surface_longitude',
                              'surface_x','surface_y','x_points','y_points',
                              'zone_number','zone_letter','latitude_points','longitude_points']
                              
    survey_dict = {}
    for field_name in survey_fields_list:
        # get available dict fields from production data
        if field_name in list(survey_data_list[0].keys()):
            # convert data to np.array and update dict
            survey_dict.update({field_name: np.asarray([ROW[field_name] for ROW in survey_data_list])})

    # get ProductionMonthly dataclass object for dict
    directional_survey = DirectionalSurvey(**survey_dict)

    return directional_survey

def get_utms(row):
    """
    DESCRIPTION
    """
    
    tup = utm.from_latlon(row.iloc[0],row.iloc[1])
    return pd.Series(tup[:4])

#gets lat long from UTM coords
def get_latlon(row):
    """
    DESCRIPTION
    """
    
    tup = utm.to_latlon(row.iloc[0],row.iloc[1],row.iloc[2],row.iloc[3])
    return pd.Series(tup[:2])


def read_data(path_file):
    """
    
    """
    file = path_file
    
    df = pd.read_csv(file, sep=',')
    
    survey_dict = df.to_dict(orient='records')
    
    return survey_dict

# # filter to dict to select keys and create list of dicts
# keys = ['wellId','md','inc','azim','surface_latitude','surface_longitude','latitude_decimal_deg','longitude_decimal_deg']
# survey_dict = [(dict((k, d[k]) for k in keys if k in d)) for d in my_data]
# survey_dict