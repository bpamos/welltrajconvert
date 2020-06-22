from src.utils import *
from src.dataclass import *
import json
#import scipy
from scipy.ndimage.interpolation import shift

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
        if is_dict(directional_survey_data) is True:
            # convert survey data into its dataclass obj
            directional_survey = DirectionalSurvey(**directional_survey_data)
            self.directional_survey_points = directional_survey
        else:
            self.directional_survey_points = directional_survey_data

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
        surface_latitude = self.directional_survey_points.surface_latitude
        surface_longitude = self.directional_survey_points.surface_longitude
        e_w_deviation = self.directional_survey_points.e_w_deviation
        n_s_deviation = self.directional_survey_points.n_s_deviation

        surface_x, surface_y, zone_number, zone_letter = utm.from_latlon(surface_latitude[0], surface_longitude[0])

        # create X and Y columns for each deviation point
        # add the x and y offset from the surface x and y for each point * meters conversion
        # TODO add meters or feet conversion. Currenlty assumes offset feet and converts to meters
        x_points = np.multiply(e_w_deviation, 0.3048) + surface_x
        y_points = np.multiply(n_s_deviation, 0.3048) + surface_y

        latitude_points, longitude_points = utm.to_latlon(x_points, y_points, zone_number, zone_letter)


        directional_survey = DirectionalSurvey(wellId=self.directional_survey_points.wellId,
                                               md=self.directional_survey_points.md,
                                               inc=self.directional_survey_points.inc,
                                               azim=self.directional_survey_points.azim,
                                               surface_latitude=self.directional_survey_points.surface_latitude,
                                               surface_longitude=self.directional_survey_points.surface_longitude,
                                               tvd=self.directional_survey_points.tvd,
                                               dls=self.directional_survey_points.dls,
                                               longitude_points=longitude_points,
                                               latitude_points=latitude_points,
                                               zone_number=zone_number,
                                               zone_letter=zone_letter,
                                               x_points=x_points,
                                               y_points=y_points,
                                               surface_x=surface_x,
                                               surface_y=surface_y
                                               )

        survey_obj = Survey(directional_survey)

        return survey_obj

    def minimum_curvature_algo(self):
        # Following are the calculations for Minimum Curvature Method

        wellId = self.directional_survey_points.wellId
        md = self.directional_survey_points.md
        inc = self.directional_survey_points.inc
        azim = self.directional_survey_points.azim
        surface_latitude = self.directional_survey_points.surface_latitude
        surface_longitude = self.directional_survey_points.surface_longitude

        # Convert to Radians
        inc_rad = np.multiply(self.directional_survey_points.inc, 0.0174533)
        azim_rad = np.multiply(self.directional_survey_points.azim, 0.0174533)

        # Shift all array values +1
        md_shift = shift(md, 1, cval=np.NaN)
        inc_shift = shift(inc, 1, cval=np.NaN)
        azim_shift = shift(azim, 1, cval=np.NaN)
        inc_rad_shift = shift(inc_rad, 1, cval=np.NaN)
        inc_rad_shift = shift(inc_rad, 1, cval=np.NaN)
        azim_rad_shift = shift(azim_rad, 1, cval=np.NaN)

        # calculate beta (dog leg angle)
        beta = np.arccos(
            np.cos(inc_rad - inc_rad_shift - (np.sin(inc_rad_shift) *
                                              np.sin(inc_rad) *
                                              (1 - np.cos(azim_rad - azim_rad_shift))
                                              )))

        # convert first nan value to 0
        beta[np.isnan(beta)] = 0

        # dog leg severity per 100 ft
        dls = (beta * 57.2958 * 100) / (md - md_shift)
        dls[np.isnan(dls)] = 0

        # calculate ratio factor (radians)
        # replace 0 for rf calc
        beta_no_zero = np.where(beta == 0, 1, beta)
        rf = np.where(beta == 0, 1, 2 / beta_no_zero * np.tan(beta_no_zero / 2))

        # calculate total vertical depth
        tvd = ((md - md_shift) / 2) * (np.cos(inc_rad_shift) + np.cos(inc_rad)) * rf
        tvd[np.isnan(tvd)] = 0

        tvd_cum = np.cumsum(tvd, dtype=float)

        # calculating NS
        ns = ((md - md_shift) / 2) * (
                    np.sin(inc_rad_shift) * np.cos(azim_rad_shift) + np.sin(inc_rad) * np.cos(azim_rad)) * rf
        ns[np.isnan(ns)] = 0

        n_s_deviation = np.cumsum(ns, dtype=float)

        # calculating EW
        ew = ((md - md_shift) / 2) * (
                    np.sin(inc_rad_shift) * np.sin(azim_rad_shift) + np.sin(inc_rad) * np.sin(azim_rad)) * rf
        ew[np.isnan(ew)] = 0

        e_w_deviation = np.cumsum(ew, dtype=float)


        # 'inc_rad': inc_rad,
        # 'azim_rad': azim_rad,
        # 'beta': beta,
        # 'rf': rf,
        # 'tvd_cum': tvd_cum,
        # 'ew': ew,
        # 'ns': ns
        directional_survey = DirectionalSurvey(wellId=self.directional_survey_points.wellId,
                                               md=md,
                                               inc=inc,
                                               azim=azim,
                                               surface_latitude=surface_latitude,
                                               surface_longitude=surface_longitude,
                                               tvd=tvd,
                                               dls=dls,
                                               e_w_deviation=e_w_deviation,
                                               n_s_deviation=n_s_deviation)

        survey_obj = Survey(directional_survey)

        survey_obj = survey_obj.get_lat_lon_from_deviation()

        return survey_obj


    def get_survey_df(self):

        survey_df = pd.DataFrame({'wellId': self.directional_survey_points.wellId,
                                  'md': self.directional_survey_points.md,
                                  'inc': self.directional_survey_points.inc,
                                  'azim': self.directional_survey_points.azim,
                                  'e_w_deviation': self.directional_survey_points.e_w_deviation,
                                  'n_s_deviation': self.directional_survey_points.n_s_deviation,
                                  'dls': self.directional_survey_points.dls,
                                  'surface_latitude': self.directional_survey_points.surface_latitude,
                                  'surface_longitude': self.directional_survey_points.surface_longitude,
                                  'longitude_points': self.directional_survey_points.longitude_points,
                                  'latitude_points': self.directional_survey_points.latitude_points,
                                  'zone_number': self.directional_survey_points.zone_number,
                                  'zone_letter': self.directional_survey_points.zone_letter,
                                  'x_points': self.directional_survey_points.x_points,
                                  'y_points': self.directional_survey_points.y_points,
                                  'surface_x': self.directional_survey_points.surface_x,
                                  'surface_y': self.directional_survey_points.surface_y
                                  })
        return survey_df