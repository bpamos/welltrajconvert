from src.core import *


@dataclass
class DataObject(metaclass=abc.ABCMeta):
    """
    Dataclass for Directional DirectionalSurvey Points, takes a list of dictionaries and converts them into np.arrays
    The data class accepts common directional survey params, some are required. Using the required inputs
    a minimum curvature algorithim will be applied to the data, providing latitude and longitude points
    along the wellbore and additional useful parameters.
    Intended to be run per well.

    Args:
    wellId:             (required) Unique well identification id
    md:                 (required) measured depth  is the actual depth of the hole drilled to any point along 
                        the wellbore or to total depth, as measured from the surface location
    inc:                (required) inclination angle, the angular measurement that the borehole deviates from vertical.
    azim:               (required) azimuth degrees, the hole direction is measured in degrees (0 to 360°)
    tvd:                true vertical depth from surface to the survey point.
    n_s_deviation:      north south deviation for each point in the wellbore path.
    x_offset:           The X offset for each point in the bore path.
    e_w_deviation:      east west deviation for each point in the wellbore path.
    y_offset:           The Y offset for each point in the wellbore path.
    dls:                Dogleg severity is a measure of the change in direction of a wellbore 
                        over a defined length, measured in degrees per 100 feet of length.
    surface_latitude:   (required) surface hole latitude
    surface_longitude:  (required) surface hole longitude
    surface_x:          Surface Easting component of the UTM coordinate
    surface_y:          Surface Northing component of the UTM coordinate
    x_points:           Easting component of the UTM coordinate
    y_points:           Northing component of the UTM coordinate
    zone_number:        Zone number of the UTM coordinate
    zone_letter:        Zone letter of the UTM coordinate
    latitude_points:    The latitude value of a location in the borehole.
                        A positive value denotes north.
                        Angle subtended with equatorial plane by a perpendicular
                        from a point on the surface of a spheriod.
    longitude_points:   The longitude value of a location in a borehole.
                        A positive value denotes east.
                        Angle measured about the spheroid axis from
                        a local prime meridian to the meridian through the point.

    Returns:
    dataclass obj:      Dataclass Directional DirectionalSurvey object
    """

    # TODO: enforce md, inc, and azim to be same length
    # TODO: enforce md to be postitive, inc to be between 0 and 100, azim to be between 0 and 360
    # TODO: enforce lat and lon to be between some values as well.
    wellId: str
    md: np.ndarray
    inc: np.ndarray
    azim: np.ndarray
    surface_latitude: float
    surface_longitude: float
    tvd: np.ndarray = field(default=None, metadata={'unit': 'float'})
    n_s_deviation: np.ndarray = field(default=None, metadata={'unit': 'float'})
    ## n_s: np.ndarray = field(default=None, metadata={'unit': 'str'}) # not used, remove?
    ## x_offset: np.ndarray = field(default=None, metadata={'unit': 'float'}) # not used, remove?
    e_w_deviation: np.ndarray = field(default=None, metadata={'unit': 'float'})
    ## e_w: np.ndarray = field(default=None, metadata={'unit': 'str'}) # not used, remove?
    ## y_offset: np.ndarray = field(default=None, metadata={'unit': 'float'}) # not used, remove?
    # TODO: dls looks like build rate with no negatives (look into)
    dls: np.ndarray = field(default=None, metadata={'unit': 'float'})
    surface_x: float = field(default=None, metadata={'unit': 'float'})
    surface_y: float = field(default=None, metadata={'unit': 'float'})
    x_points: np.ndarray = field(default=None, metadata={'unit': 'float'})
    y_points: np.ndarray = field(default=None, metadata={'unit': 'float'})
    zone_number: int = field(default=None, metadata={'unit': 'int'})
    zone_letter: str = field(default=None, metadata={'unit': 'str'})
    latitude_points: np.ndarray = field(default=None, metadata={'unit': 'float'})
    longitude_points: np.ndarray = field(default=None, metadata={'unit': 'float'})
    isHorizontal: np.ndarray = field(default=None, metadata={'unit': 'str'})




    #@abc.abstractmethod
    def validate_array_length(self):
        """

        :return:
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

        :return:
        """

        if any(neg < 0 for neg in self.md) is False:
            pass
        else:
            raise ValueError(f"Validation Error: MD array has negative values")
        if any(neg < 0 for neg in self.inc) is False:
            pass
        else:
            raise ValueError(f"Validation Error: INC array has negative values")

    def validate_azim_values(self):
        """

        :return:
        """
        #TODO correct the azim to be between 0 and 360
        if any(i > 360 or i < 0 for i in self.azim) is False:
            pass
        else:
            raise ValueError(f"Validation Error: AZIM array must have values between 0 and 360")



    def __post_init__(self):
        """
        look in all fields and types,
        if type is None pass,
        else if type given doesnt match dataclass type raise error
        """

        for (name, field_type) in self.__annotations__.items():
            if not isinstance(self.__dict__[name], field_type):
                current_type = type(self.__dict__[name])
                if current_type is type(None):
                    pass
                else:
                    raise ValueError(f"The field `{name}` was assigned by `{current_type}` instead of `{field_type}`")
        self.validate_array_length()
        self.validate_array_sign()
        self.validate_azim_values()