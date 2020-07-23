from src.imports import *


class DataObject(metaclass=abc.ABCMeta):
    """
    Info

    """
    def __init__(self, wellId: str, md: list, inc: list, azim: list,
                 surface_latitude: float, surface_longitude: float,
                 tvd: list = None, n_s_deviation: list = None, e_w_deviation: list = None, dls: list = None,
                 surface_x: float = None, surface_y: float = None, x_points: list = None, y_points: list = None,
                 zone_number: int = None, zone_letter: str = None,
                 latitude_points: list = None, longitude_points: list = None, isHorizontal: list = None):

        self.wellId = wellId
        self.md = md
        self.inc = inc
        self.azim = azim
        self.surface_latitude = surface_latitude
        self.surface_longitude = surface_longitude
        self.tvd = tvd
        self.n_s_deviation = n_s_deviation
        self.e_w_deviation = e_w_deviation
        self.dls = dls
        self.surface_x = surface_x
        self.surface_y = surface_y
        self.x_points = x_points
        self.y_points = y_points
        self.zone_number = zone_number
        self.zone_letter = zone_letter
        self.latitude_points = latitude_points
        self.longitude_points = longitude_points
        self.isHorizontal = isHorizontal

    @abstractmethod
    def validate(self):
        """
        validate different variables to ensure data put in
        will work with the directional survey functions

        """

        # a bunch of validation functions
        def validate_array_length(self):
            """
            validate the length of the array,
            ensure md, inc, and azim are equal lengths

            :return: pass or ValueError
            """
            md_len = len(self.md)
            inc_len = len(self.inc)
            azim_len = len(self.azim)
            if inc_len == md_len and azim_len == md_len:
                pass
            else:
                raise ValueError(f"Validation Error: Array lengths must be equal,"
                                 f" md length: `{md_len}` md length: `{inc_len}` md length: `{azim_len}`")

        def validate_array_sign(self):
            """
            validate md and inc are not negative

            :return: pass of ValueError
            """

            if any(neg < 0 for neg in self.md) is False:
                pass
            else:
                raise ValueError(f"Validation Error: MD array has negative values")
            if any(neg < 0 for neg in self.inc) is False:
                pass
            else:
                raise ValueError(f"Validation Error: INC array has negative values")

        def validate_lat_long_range(self):
            """
            validate that the surface lat and long are between the acceptable ranges

            :return: pass of ValueError
            """

            if -90 <= self.surface_latitude <= 90:
                pass
            else:
                raise ValueError(f"Validation Error: surface_latitude has values outside acceptable range")

            if -180 <= self.surface_longitude <= 180:
                pass
            else:
                raise ValueError(f"Validation Error: surface_longitude has values outside acceptable range")

        # TODO: is this the correct way to test this.
        def validate_wellId(self):
            """
            validate that wellId is a string, it needs to be a single wellId value
            not a list or array of wellIds

            :return: pass or TypeError
            """
            wellId_type = type(self.wellId)
            if wellId_type is str:
                pass
            else:
                raise TypeError(f"Validation Error: wellId has type {wellId_type}")

        def validate_array_monotonic(self):
            """
            check if array is monotonically increasing,
            always increasing of staying the same

            :return: True or ValueError
            """

            # get the diff between each element
            dx = np.diff(self.md)
            # if they are greater than
            if np.all(dx <= 0) or np.all(dx >= 0) == True:
                pass
            else:
                raise ValueError(f"Validation Error: MD array must monotonically increase")

        # TODO: validation for Azim between 360 and 0, if not correct it
        # TODO: validation for Inc between 0 and 90 (or 100)?

        # run validation functions
        validate_array_length(self)
        validate_array_sign(self)
        validate_wellId(self)
        validate_lat_long_range(self)
        validate_array_monotonic(self)

    @abstractmethod
    def serialize(self):

        # TODO: make this one line, if not present pass, else turn to array
        # self.tvd = ifnone('None',np.array(self.tvd))

        self.wellId = self.wellId
        self.md = np.array(self.md)
        self.inc = np.array(self.inc)
        self.azim = np.array(self.azim)
        self.surface_latitude = self.surface_latitude
        self.surface_longitude = self.surface_longitude
        # self.tvd = np.array(self.tvd)
        if self.tvd is not None:
            self.tvd = np.array(self.tvd)
        # self.n_s_deviation = np.array(self.n_s_deviation)
        if self.n_s_deviation is not None:
            self.n_s_deviation = np.array(self.n_s_deviation)
        #self.e_w_deviation = np.array(self.e_w_deviation)
        if self.e_w_deviation is not None:
            self.e_w_deviation = np.array(self.e_w_deviation)
        # self.dls = np.array(self.dls)
        if self.dls is not None:
            self.dls = np.array(self.dls)

        self.surface_x = self.surface_x
        self.surface_y = self.surface_y

        # self.x_points = np.array(self.x_points)
        if self.x_points is not None:
            self.x_points = np.array(self.x_points)
        # self.y_points = np.array(self.y_points)
        if self.y_points is not None:
            self.y_points = np.array(self.y_points)

        self.zone_number = self.zone_number
        self.zone_letter = self.zone_letter

        # self.latitude_points = np.array(self.latitude_points)
        if self.latitude_points is not None:
            self.latitude_points = np.array(self.latitude_points)
        # self.longitude_points = np.array(self.longitude_points)
        if self.longitude_points is not None:
            self.longitude_points = np.array(self.longitude_points)
        # self.isHorizontal = np.array(self.isHorizontal)
        if self.isHorizontal is not None:
            self.isHorizontal = np.array(self.isHorizontal)