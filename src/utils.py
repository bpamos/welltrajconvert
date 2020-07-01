from src.core import *
from src.data_object import *
from src.directional_survey import *


def ifnone(a:Any,b:Any)->Any:
    "`a` if `a` is not None, otherwise `b`."
    return b if a is None else a


def is_dict(object):
    """
    Helper function that checks if a given parameter is a dict or not
    """

    if isinstance(object, dict):
        return True
    else:
        return False



# def get_directional_survey_dataclass(survey_data_list):
#     """
#     iterates over a list of production data
#     looks for field names that match the ProductionMonthly dataclass fields
#     converts these key value pairs to np.arrays and puts them in an empty dict
#     returns the ProductionMonthly dataclass object for this new dict
#
#     Args:
#     survey_data_list (list of dicts) list of directional survey data dicts to iterate over
#     (data dict should should match required dict format for DataObject dataclass)
#
#     Returns:
#     DataObject dataclass object for one well
#     """
#
#     # DataObject dataclass fields
#     survey_fields_list = ['wellId', 'md', 'inc', 'azim', 'tvd',
#                           'n_s_deviation', 'n_s', 'x_offset',
#                           'e_w_deviation', 'e_w', 'y_offset', 'dls',
#                           'surface_latitude', 'surface_longitude',
#                           'surface_x', 'surface_y', 'x_points', 'y_points',
#                           'zone_number', 'zone_letter', 'latitude_points', 'longitude_points']
#
#     survey_dict = {}
#     for field_name in survey_fields_list:
#         # get available dict fields from production data
#         if field_name in list(survey_data_list[0].keys()):
#             # convert data to np.array and update dict
#             survey_dict.update({field_name: np.asarray([ROW[field_name] for ROW in survey_data_list])})
#
#     # get ProductionMonthly dataclass object for dict
#     #directional_survey = DataObject(**survey_dict)
#
#     return survey_dict

def is_dict(object):
    """
    Helper function that checks if a given parameter is a dict or not
    """

    if isinstance(object, dict):
        return True
    else:
        return False

# def get_utms(row):
#     """
#     DESCRIPTION
#     :param row:
#     :return:
#     """
#
#     tup = utm.from_latlon(row.iloc[0], row.iloc[1])
#     return pd.Series(tup[:4])


# gets lat long from UTM coords
# def get_lat_lon(row):
#     """
#     DESCRIPTION
#     """
#
#     tup = utm.to_latlon(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3])
#     return pd.Series(tup[:2])

