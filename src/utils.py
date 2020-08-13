"`.utils` contains essential util functions to format and split data"
from src.imports import *


def if_none(a: Any, b: Any) -> Any:
    "`a` if `a` is not None, otherwise `b`."
    return b if a is None else a


def to_type(a: Any, data_type):
    """
    If item is None, return None, else, convert to an data_type specified
    (ie. np.array, str, int, float, ect..)

    :parameter: a (Any or None)

    :returns: None or data_type(a)
    """
    return None if a is None else data_type(a)


def is_dict(obj):
    """
    Helper function that checks if a given parameter is a dict or not
    """

    if isinstance(obj, dict):
        return True
    else:
        return False

def crs_transformer(crs_out: str, crs_in: str, x: float, y: float):
    """
    takes a two crs and transforms x and y coordinates to latitude and longitude.
    find the crs_in of interst at `https://epsg.io/`

    """
    transformer = Transformer.from_crs(crs_in, crs_out)
    latitude, longitude = transformer.transform(x, y)

    return latitude, longitude


## external helper functions for using the library:

# def from_multiple_wells(df: DataFrame, wellId_name: Optional[str] = None, md_name: Optional[str] = None,
#                         inc_name: Optional[str] = None, azim_name: Optional[str] = None,
#                         surface_latitude_name: Optional[str] = None,
#                         surface_longitude_name: Optional[str] = None,
#                         surface_x_name: Optional[str] = None,
#                         surface_y_name: Optional[str] = None):
#     # group by wellId, ensures this will work with single well or mulitple.
#     grouped = df.groupby(wellId_name)
#
#     # initialize empty dict and list
#     d = {}
#     dlist = []
#     # loop through groups converting them to the proper dict format
#     for name, group in grouped:
#
#         group.reset_index(inplace=True, drop=True)
#
#         if surface_latitude_name is not None and surface_longitude_name is not None:
#             well_obj = WellboreTrajectory.from_df(group, wellId_name=wellId_name, md_name=md_name,
#                                                   inc_name=inc_name, azim_name=azim_name,
#                                                   surface_latitude_name=surface_latitude_name,
#                                                   surface_longitude_name=surface_longitude_name)
#         if surface_x_name is not None and surface_y_name is not None:
#             well_obj = WellboreTrajectory.from_df(group, wellId_name=wellId_name, md_name=md_name,
#                                                   inc_name=inc_name, azim_name=azim_name,
#                                                   surface_x_name=surface_x_name,
#                                                   surface_y_name=surface_y_name)
#
#         well_obj.calculate_survey_points()
#         dataclass_obj = well_obj.deviation_survey_obj
#
#         # TODO: convert to dict???
#         d = dataclass_obj
#         dlist.append(d)
#
#     res = {'data': dlist}
#     return res


# def from_multiple_wells_to_df(df: DataFrame, wellId_name: Optional[str] = None, md_name: Optional[str] = None,
#                               inc_name: Optional[str] = None, azim_name: Optional[str] = None,
#                               surface_latitude_name: Optional[str] = None,
#                               surface_longitude_name: Optional[str] = None,
#                               surface_x_name: Optional[str] = None,
#                               surface_y_name: Optional[str] = None):
#     # group by wellId, ensures this will work with single well or mulitple.
#     grouped = df.groupby(wellId_name)
#
#     # initialize empty dict and list
#     appended_df = pd.DataFrame()
#     # loop through groups converting them to the proper dict format
#     for name, group in grouped:
#
#         group.reset_index(inplace=True, drop=True)
#
#         if surface_latitude_name is not None and surface_longitude_name is not None:
#             well_obj = WellboreTrajectory.from_df(group, wellId_name=wellId_name, md_name=md_name,
#                                                   inc_name=inc_name, azim_name=azim_name,
#                                                   surface_latitude_name=surface_latitude_name,
#                                                   surface_longitude_name=surface_longitude_name)
#         if surface_x_name is not None and surface_y_name is not None:
#             well_obj = WellboreTrajectory.from_df(group, wellId_name=wellId_name, md_name=md_name,
#                                                   inc_name=inc_name, azim_name=azim_name,
#                                                   surface_x_name=surface_x_name,
#                                                   surface_y_name=surface_y_name)
#
#         well_obj.calculate_survey_points()
#         well_obj.deviation_survey_obj
#         appended_df = appended_df.append(well_obj.get_survey_df())
#
#     res = appended_df
#     return res