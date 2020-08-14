from src.data_object import *


@dataclass
class DeviationSurvey(DataObject):
    """
    Dataclass for Directional Survey Points takes a single `DataObject` and validates and serializes it.
    Then converts it into a Dataclass object of Deviation Survey points, ensuring that all the correct data types
    are present for later calculations.

    :parameter:
    wellId:             (required) Unique well identification id
    md:                 (required) measured depth  is the actual depth of the hole drilled to any point along
                        the wellbore or to total depth, as measured from the surface location
    inc:                (required) inclination angle, the angular measurement that the borehole deviates from vertical.
    azim:               (required) azimuth degrees, the hole direction is measured in degrees (0 to 360°)
    surface_latitude:   (required) surface hole latitude
    surface_longitude:  (required) surface hole longitude
    tvd:                true vertical depth from surface to the survey point.
    n_s_deviation:      north south deviation for each point in the wellbore path.
    e_w_deviation:      east west deviation for each point in the wellbore path.
    dls:                Dogleg severity is a measure of the change in direction of a wellbore
                        over a defined length, measured in degrees per 100 feet of length.
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
    IsHorizontal:       Array of strings, Vertical Or Horizontal depending on Inclination angle point

    :returns:
    dataclass obj:      Dataclass DirectionalSurvey object
    """

    wellId: str
    md: np.ndarray
    inc: np.ndarray
    azim: np.ndarray
    surface_latitude: float = field(default=None, metadata={'unit': 'float'})
    surface_longitude: float = field(default=None, metadata={'unit': 'float'})
    tvd: np.ndarray = field(default=None, metadata={'unit': 'float'})
    n_s_deviation: np.ndarray = field(default=None, metadata={'unit': 'float'})
    e_w_deviation: np.ndarray = field(default=None, metadata={'unit': 'float'})
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

    def from_json(self):
        super().from_json()

    def deserialize(self):
        super().deserialize()

    def validate(self):
        """
        validate different parameters to ensure that the data in the DataObject
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
                                 f" md length: `{md_len}` inc length: `{inc_len}` azim length: `{azim_len}`")

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
            if self.surface_latitude is not None and self.surface_longitude is not None:
                if -90 <= self.surface_latitude <= 90:
                    pass
                else:
                    raise ValueError(f"Validation Error: surface_latitude"
                                     f" has values outside acceptable range: {self.surface_latitude}")

                if -180 <= self.surface_longitude <= 180:
                    pass
                else:
                    raise ValueError(f"Validation Error: surface_longitude "
                                     f"has values outside acceptable range: {self.surface_longitude}")

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
            # if they are greater than zero, then the array is always increasing in the positive direction
            if np.all(dx >= 0) == True:
                pass
            else:
                raise ValueError(f"Validation Error: MD array must monotonically increase")

        # TODO: validation for Azim between 360 and 0, if not correct it
        # TODO: validation for Inc between 0 and 90 (or 100)?
        # TODO: no NaNs

        # run validation functions
        validate_array_length(self)
        validate_array_sign(self)
        validate_wellId(self)
        validate_lat_long_range(self)
        validate_array_monotonic(self)

    def serialize(self):
        """
        convert dict values to their proper serialized dict values
        converts lists to np.arrays if not None
        converts value to float if not None
        converts value to int if not None
        converts value to str if not None

        :parameter:
        DataObject params

        :return:
        DataObject params serialized as floats, str, int, or np.arrays
        """

        self.wellId = to_type(self.wellId, str)
        self.md = to_type(self.md, np.array)
        self.inc = to_type(self.inc, np.array)
        self.azim = to_type(self.azim, np.array)
        self.surface_latitude = to_type(self.surface_latitude, float)
        self.surface_longitude = to_type(self.surface_longitude, float)
        self.tvd = to_type(self.tvd, np.array)
        self.n_s_deviation = to_type(self.n_s_deviation, np.array)
        self.e_w_deviation = to_type(self.e_w_deviation, np.array)
        self.dls = to_type(self.dls, np.array)
        self.surface_x = to_type(self.surface_x, float)
        self.surface_y = to_type(self.surface_y, float)
        self.x_points = to_type(self.x_points, np.array)
        self.y_points = to_type(self.y_points, np.array)
        self.zone_number = to_type(self.zone_number, int)
        self.zone_letter = to_type(self.zone_letter, str)
        self.latitude_points = to_type(self.latitude_points, np.array)
        self.longitude_points = to_type(self.longitude_points, np.array)
        self.isHorizontal = to_type(self.isHorizontal, np.array)

    def __post_init__(self):
        """
        validate all data,
        serialized all validated data,
        look in all fields and types,
        if type is None pass,
        else if type given doesnt match dataclass type raise error
        """
        self.validate()
        self.serialize()
        for (name, field_type) in self.__annotations__.items():
            if not isinstance(self.__dict__[name], field_type):
                current_type = type(self.__dict__[name])
                if current_type is type(None):
                    pass
                else:
                    raise ValueError(f"The field `{name}` was assigned by `{current_type}` instead of `{field_type}`")
