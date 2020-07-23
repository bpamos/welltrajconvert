# from src.utils import *
# from src.data_object import *
# from src.deviation_survey import *
#
# # put in data object
# class DirectionalSurvey(DeviationSurvey):
#     """
#     Get information about a directional survey from dict or dataclass obj
#     and reformat into directional survey obj
#     """
#
#     def __init__(self, directional_survey_data):
#         """
#         DirectionalSurvey object with a wells directional survey info
#
#         Attributes:
#         directional_survey_points (Dataclass Object) DataObject object
#         """
#
#         self.directional_survey_points = DeviationSurvey(directional_survey_data)
#
#     def calculate_lat_lon_from_deviation_points(self, e_w_deviation, n_s_deviation):
#         """
#         get lat lon points from survey using minimum curvature algorithm generated values
#         for the ns and ew deviations
#
#         :parameter:
#         e_w_deviation:          (np.array)
#         n_s_deviation:          (np.array)
#
#         required survey data:
#         self.surface_latitude:  (float)
#         self.surface_longitude: (float)
#
#         :return:
#         Calculated attributes for lat lon points
#         longitude_points:       (np.array)
#         latitude_points:        (np.array)
#         zone_number:            (str)
#         zone_letter:            (str)
#         x_points:               (np.array)
#         y_points:               (np.array)
#         surface_x:              (np.array)
#         surface_y:              (np.array)
#         """
#         surface_latitude = self.directional_survey_points.surface_latitude
#         surface_longitude = self.directional_survey_points.surface_longitude
#
#         # create X and Y deviation points and zone number and letter
#         surface_x, surface_y, zone_number, zone_letter = utm.from_latlon(surface_latitude, surface_longitude)
#
#         # add the x and y offset from the surface x and y for each point * meters conversion
#         x_points = np.multiply(e_w_deviation, 0.3048) + surface_x
#         y_points = np.multiply(n_s_deviation, 0.3048) + surface_y
#
#         # create lat lon points along the wellbore from the x,y,zone number and leter
#         latitude_points, longitude_points = utm.to_latlon(x_points, y_points, zone_number, zone_letter)
#
#         return (longitude_points, latitude_points,
#                 zone_number, zone_letter,
#                 x_points, y_points,
#                 surface_x, surface_y)
#
#     def minimum_curvature_algo(self):
#         """
#         Calculate values along the wellbore using only provided md, inc, and azim
#         calculate TVD, n_s_deviation, e_w_deviation, and dls
#
#         :parameter:
#         None
#
#         :return:
#         tvd_cum:            (np.array)
#         dls:                (np.array)
#         e_w_deviation:      (np.array)
#         n_s_deviation:      (np.array)
#         """
#         # Following are the calculations for Minimum Curvature Method
#
#         md = self.directional_survey_points.md
#         inc = self.directional_survey_points.inc
#         azim = self.directional_survey_points.azim
#
#         # Convert to Radians
#         inc_rad = np.multiply(inc, 0.0174533)
#         azim_rad = np.multiply(azim, 0.0174533)
#
#         # Shift all array values +1
#         md_shift = shift(md, 1, cval=np.NaN)
#         inc_rad_shift = shift(inc_rad, 1, cval=np.NaN)
#         azim_rad_shift = shift(azim_rad, 1, cval=np.NaN)
#
#         # calculate beta (dog leg angle)
#         beta = np.arccos(
#             np.cos(inc_rad - inc_rad_shift - (np.sin(inc_rad_shift) *
#                                               np.sin(inc_rad) *
#                                               (1 - np.cos(azim_rad - azim_rad_shift))
#                                               )))
#
#         # convert first nan value to 0
#         beta[np.isnan(beta)] = 0
#
#         # dog leg severity per 100 ft
#         dls = (beta * 57.2958 * 100) / (md - md_shift)
#         dls[np.isnan(dls)] = 0
#
#         # calculate ratio factor (radians)
#         # replace 0 for rf calc
#         beta_no_zero = np.where(beta == 0, 1, beta)
#         rf = np.where(beta == 0, 1, 2 / beta_no_zero * np.tan(beta_no_zero / 2))
#
#         # calculate total vertical depth
#         tvd = ((md - md_shift) / 2) * (np.cos(inc_rad_shift) + np.cos(inc_rad)) * rf
#         tvd[np.isnan(tvd)] = 0
#
#         tvd_cum = np.cumsum(tvd, dtype=float)
#
#         # calculating NS
#         ns = ((md - md_shift) / 2) * (
#                 np.sin(inc_rad_shift) * np.cos(azim_rad_shift) +
#                 np.sin(inc_rad) * np.cos(azim_rad)) * rf
#         ns[np.isnan(ns)] = 0
#
#         n_s_deviation = np.cumsum(ns, dtype=float)
#
#         # calculating EW
#         ew = ((md - md_shift) / 2) * (
#                 np.sin(inc_rad_shift) * np.sin(azim_rad_shift) +
#                 np.sin(inc_rad) * np.sin(azim_rad)) * rf
#         ew[np.isnan(ew)] = 0
#
#         e_w_deviation = np.cumsum(ew, dtype=float)
#
#         return tvd_cum, dls, e_w_deviation, n_s_deviation
#
#     def calculate_horizontal(self):
#         """
#         calculate if the inclination of the wellbore is in its horizontal section
#         If the wellbore inclination is greater than 88 degrees the wellbore is horizontal
#         else the well is vertical
#
#         :parameter:
#         None
#
#         :return:
#         inc_hz:     (np.array)
#         """
#         # get inc points
#         inc = self.directional_survey_points.inc
#
#         # inc greater than 88 deg is horizontal, else vertical
#         inc_hz = np.greater(inc, 88)
#         inc_hz = np.where((inc_hz == True), 'Horizontal', 'Vertical')
#
#         return inc_hz
#
#     def calculate_survey_points(self):
#         """
#         Run the minimum_curvature_algo, calculate_lat_lon_from_deviation_points, and calculate_horizontal
#         functions to calculate the wells lat lon points and other attributes from provided md, inc, azim
#         and surface lat lon
#
#         :parameter:
#         None
#
#         :return:
#         survey_points_obj:       (DirectionalSurvey obj)
#
#         """
#
#         # get minimum curvature points
#         tvd_cum, dls, e_w_deviation, n_s_deviation = self.minimum_curvature_algo()
#
#         # get lat lon points
#         (longitude_points, latitude_points,
#          zone_number, zone_letter,
#          x_points, y_points,
#          surface_x, surface_y) = self.calculate_lat_lon_from_deviation_points(e_w_deviation, n_s_deviation)
#
#         inc_hz = self.calculate_horizontal()
#
#         directional_survey = DataObject(wellId=self.directional_survey_points.wellId,
#                                         md=self.directional_survey_points.md,
#                                         inc=self.directional_survey_points.inc,
#                                         azim=self.directional_survey_points.azim,
#                                         surface_latitude=self.directional_survey_points.surface_latitude,
#                                         surface_longitude=self.directional_survey_points.surface_longitude,
#                                         e_w_deviation=e_w_deviation,
#                                         n_s_deviation=n_s_deviation,
#                                         tvd=tvd_cum,
#                                         dls=dls,
#                                         longitude_points=longitude_points,
#                                         latitude_points=latitude_points,
#                                         zone_number=zone_number,
#                                         zone_letter=zone_letter,
#                                         x_points=x_points,
#                                         y_points=y_points,
#                                         surface_x=surface_x,
#                                         surface_y=surface_y,
#                                         isHorizontal=inc_hz
#                                         )
#         # convert to survey obj
#         survey_points_obj = DirectionalSurvey(directional_survey)
#
#         return survey_points_obj
#
#     def get_survey_df(self):
#         """
#         Convert survey object to dataframe
#
#         :parameter:
#         None
#
#         :return:
#         survey_df:      (dataframe)
#
#         """
#
#         survey_df = pd.DataFrame({'wellId': self.directional_survey_points.wellId,
#                                   'md': self.directional_survey_points.md,
#                                   'inc': self.directional_survey_points.inc,
#                                   'azim': self.directional_survey_points.azim,
#                                   'tvd': self.directional_survey_points.tvd,
#                                   'e_w_deviation': self.directional_survey_points.e_w_deviation,
#                                   'n_s_deviation': self.directional_survey_points.n_s_deviation,
#                                   'dls': self.directional_survey_points.dls,
#                                   'surface_latitude': self.directional_survey_points.surface_latitude,
#                                   'surface_longitude': self.directional_survey_points.surface_longitude,
#                                   'longitude_points': self.directional_survey_points.longitude_points,
#                                   'latitude_points': self.directional_survey_points.latitude_points,
#                                   'zone_number': self.directional_survey_points.zone_number,
#                                   'zone_letter': self.directional_survey_points.zone_letter,
#                                   'x_points': self.directional_survey_points.x_points,
#                                   'y_points': self.directional_survey_points.y_points,
#                                   'surface_x': self.directional_survey_points.surface_x,
#                                   'surface_y': self.directional_survey_points.surface_y,
#                                   'isHorizontal': self.directional_survey_points.isHorizontal
#                                   })
#
#         return survey_df
