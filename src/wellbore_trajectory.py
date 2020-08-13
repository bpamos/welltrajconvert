from src.calculable_object import *
from src.base import *


class WellboreTrajectory(CalculableObject):

    def __init__(self, data=None):
        """
        DirectionalSurvey object with a wells directional survey info

        Attributes:
        directional_survey_points (Dataclass Object) DataObject object
        """

        self.data = data
        self.deviation_survey_obj = DeviationSurvey(**self.data)

    def crs_transform(self, crs_in: str):
        crs_out = "EPSG:4326"

        x = self.deviation_survey_obj.surface_x
        y = self.deviation_survey_obj.surface_y
        self.deviation_survey_obj.surface_latitude, self.deviation_survey_obj.surface_longitude = \
            crs_transformer(crs_out=crs_out, crs_in=crs_in, x=x, y=y)


    def minimum_curvature_algo(self):
        """
        Calculate values along the wellbore using only provided md, inc, and azim
        calculate TVD, n_s_deviation, e_w_deviation, and dls

        :parameter:
        None

        :return:
        tvd_cum:            (np.array)
        dls:                (np.array)
        e_w_deviation:      (np.array)
        n_s_deviation:      (np.array)
        """
        # Following are the calculations for Minimum Curvature Method

        md = self.deviation_survey_obj.md
        inc = self.deviation_survey_obj.inc
        azim = self.deviation_survey_obj.azim

        # Convert to Radians
        inc_rad = np.multiply(inc, 0.0174533)
        azim_rad = np.multiply(azim, 0.0174533)

        # Shift all array values +1
        md_shift = shift(md, 1, cval=np.NaN)
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

        tvd = np.cumsum(tvd, dtype=float)

        # calculating NS
        ns = ((md - md_shift) / 2) * (
                np.sin(inc_rad_shift) * np.cos(azim_rad_shift) +
                np.sin(inc_rad) * np.cos(azim_rad)) * rf
        ns[np.isnan(ns)] = 0

        n_s_deviation = np.cumsum(ns, dtype=float)

        # calculating EW
        ew = ((md - md_shift) / 2) * (
                np.sin(inc_rad_shift) * np.sin(azim_rad_shift) +
                np.sin(inc_rad) * np.sin(azim_rad)) * rf
        ew[np.isnan(ew)] = 0

        e_w_deviation = np.cumsum(ew, dtype=float)

        self.deviation_survey_obj.tvd = tvd
        self.deviation_survey_obj.dls = dls
        self.deviation_survey_obj.e_w_deviation = e_w_deviation
        self.deviation_survey_obj.n_s_deviation = n_s_deviation

    def calculate_lat_lon_from_deviation_points(self):
        """
        get lat lon points from survey using minimum curvature algorithm generated values
        for the ns and ew deviations

        :parameter:
        e_w_deviation:          (np.array)
        n_s_deviation:          (np.array)

        required survey data:
        self.surface_latitude:  (float)
        self.surface_longitude: (float)

        :return:
        Calculated attributes for lat lon points
        longitude_points:       (np.array)
        latitude_points:        (np.array)
        zone_number:            (str)
        zone_letter:            (str)
        x_points:               (np.array)
        y_points:               (np.array)
        surface_x:              (np.array)
        surface_y:              (np.array)
        """
        surface_latitude = self.deviation_survey_obj.surface_latitude
        surface_longitude = self.deviation_survey_obj.surface_longitude
        e_w_deviation = self.deviation_survey_obj.e_w_deviation
        n_s_deviation = self.deviation_survey_obj.n_s_deviation

        # create X and Y deviation points and zone number and letter
        surface_x, surface_y, zone_number, zone_letter = utm.from_latlon(surface_latitude, surface_longitude)

        # add the x and y offset from the surface x and y for each point * meters conversion
        x_points = np.multiply(e_w_deviation, 0.3048) + surface_x
        y_points = np.multiply(n_s_deviation, 0.3048) + surface_y

        # create lat lon points along the wellbore from the x,y,zone number and leter
        latitude_points, longitude_points = utm.to_latlon(x_points, y_points, zone_number, zone_letter)

        self.deviation_survey_obj.longitude_points = longitude_points
        self.deviation_survey_obj.latitude_points = latitude_points
        self.deviation_survey_obj.zone_number = zone_number
        self.deviation_survey_obj.zone_letter = zone_letter
        self.deviation_survey_obj.x_points = x_points
        self.deviation_survey_obj.y_points = y_points
        self.deviation_survey_obj.surface_x = surface_x
        self.deviation_survey_obj.surface_y = surface_y

    def calculate_horizontal(self,  horizontal_angle: Optional[float] = 88.0):
        """
        calculate if the inclination of the wellbore is in its horizontal section
        If the wellbore inclination is greater than 88 degrees the wellbore is horizontal
        else the well is vertical

        :parameter:
        None

        :return:
        inc_hz:     (np.array)
        """
        # get inc points
        inc = self.deviation_survey_obj.inc

        # inc greater than 88 deg is horizontal, else vertical
        inc_hz = np.greater(inc, horizontal_angle)
        inc_hz = np.where((inc_hz == True), 'Horizontal', 'Vertical')

        self.deviation_survey_obj.isHorizontal = inc_hz

    #@abstractmethod
    def calculate_survey_points(self, **kwargs):
        """
        Run the minimum_curvature_algo, calculate_lat_lon_from_deviation_points, and calculate_horizontal
        functions to calculate the wells lat lon points and other attributes from provided md, inc, azim
        and surface lat lon

        :parameter:
        None

        :return:
        survey_points_obj:       (DirectionalSurvey obj)

        """
        for k,v in kwargs.items():
            print(k,v)

        if self.deviation_survey_obj.surface_latitude is None and self.deviation_survey_obj.surface_longitude is None:
            self.crs_transform(**kwargs)

        # get minimum curvature points
        self.minimum_curvature_algo()

        # get lat lon points
        self.calculate_lat_lon_from_deviation_points()

        # calc horizontal
        self.calculate_horizontal()


    # @classmethod
    # def from_df(cls, df, wellId_name: str = None, md_name: str = None,
    #             inc_name: str = None, azim_name: str = None,
    #             surface_latitude_name: Optional[str] = None,
    #             surface_longitude_name: Optional[str] = None,
    #             surface_x_name: Optional[str] = None,
    #             surface_y_name: Optional[str] = None):
    #     """
    #     convert a well survey df into a list of dicts format used in `WellboreTrajectory`
    #     User must specify column names for wellId, md, inc, azim, and either both
    #     surface_latitude, surface_longitude, or both surface_x, surface_y
    #
    #     :Parameters:
    #     df
    #     wellId_name
    #     md_name
    #     inc_name
    #     azim_name
    #     surface_latitude_name
    #     surface_longitude_name
    #     surface_x_name
    #     surface_y_name
    #
    #     :Return:
    #     list of dicts
    #
    #     """
    #     # if no column names are specified use 0:5 for dir survey obj
    #     surface_latitude_name = if_none(surface_latitude_name, None)
    #     surface_longitude_name = if_none(surface_longitude_name, None)
    #     surface_x_name = if_none(surface_x_name, None)
    #     surface_y_name = if_none(surface_y_name, None)
    #
    #     cols = list(df.columns)
    #     # check to make sure no columns have NaN values
    #     inputs = df.iloc[:,df_names_to_idx(cols, df)]
    #     assert not inputs.isna().any().any(), f"You have NaN values in column(s) {cols} of your dataframe, please fix it."
    #
    #     if surface_latitude_name is not None and surface_longitude_name is not None:
    #         dataclass_obj = dict(wellId=df[wellId_name][0],
    #                              md=np.array(df[md_name]),
    #                              inc=np.array(df[inc_name]),
    #                              azim=np.array(df[azim_name]),
    #                              surface_latitude=df[surface_latitude_name][0],
    #                              surface_longitude=df[surface_longitude_name][0])
    #
    #     if surface_x_name is not None and surface_y_name is not None:
    #         dataclass_obj = dict(wellId=df[wellId_name][0],
    #                              md=np.array(df[md_name]),
    #                              inc=np.array(df[inc_name]),
    #                              azim=np.array(df[azim_name]),
    #                              surface_x=df[surface_x_name][0],
    #                              surface_y=df[surface_y_name][0])
    #
    #     res = cls(data=dataclass_obj)
    #     return res
    #
    # @classmethod
    # def from_csv(cls, path: PathOrStr, wellId_name: Optional[str] = None, md_name: Optional[str] = None,
    #              inc_name: Optional[str] = None, azim_name: Optional[str] = None,
    #              surface_latitude_name: Optional[str] = None,
    #              surface_longitude_name: Optional[str] = None,
    #              surface_x_name: Optional[str] = None,
    #              surface_y_name: Optional[str] = None):
    #
    #     df = pd.read_csv(path, sep=',')
    #
    #     return cls.from_df(df, wellId_name=wellId_name, md_name=md_name,
    #                        inc_name=inc_name, azim_name=azim_name,
    #                        surface_latitude_name=surface_latitude_name,
    #                        surface_longitude_name=surface_longitude_name,
    #                        surface_x_name=surface_x_name,
    #                        surface_y_name=surface_y_name)

    # def calculate_survey_points(self):
    #     super().calculate_survey_points()
