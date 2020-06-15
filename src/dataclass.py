from dataclasses import dataclass, field
import numpy as np

@dataclass
class DirectionalSurvey:
    """
    Dataclass for Directional Survey Points, takes a list of dictionaries and converts them into np.arrays
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
    surface_x: Surface  Easting component of the UTM coordinate
    surface_y: Surface  Northing component of the UTM coordinate
    x_points:           Easting component of the UTM coordinate
    y_points:           Northing component of the UTM coordinate
    zone_number:        Zone number of the UTM coordinate
    zone_letter:        Zone letter of the UTM coordinate
    latitude_points:    The latitude value of a location in the borehole. A positive value denotes north. 
                        Angle subtended with equatorial plane by a perpendicular from a point on the surface of a spheriod.
    longitude_points:   The longitude value of a location in a borehole. A positive value denotes east. 
                        Angle measured about the spheroid axis from a local prime meridian to the meridian through the point.
    other:              Other additional fields provided in the original dataset. Kept unchanged with the prefix "other." added.

    Returns:
    dataclass obj:      Dataclass Directional Survey object
    """

    # TODO: when a default value is set to none it creates array(None), needs to be array(None,None,ect...)
    # how is the none supposed to work within the data class array.

    wellId: np.array
    md: np.array
    inc: np.array
    azim: np.array
    tvd: np.array = field(default=None, metadata={'unit': 'float'})
    n_s_deviation: np.array = field(default=None, metadata={'unit': 'float'})
    n_s: np.array = field(default=None, metadata={'unit': 'str'})
    x_offset: np.array = field(default=None, metadata={'unit': 'float'})
    e_w_deviation: np.array = field(default=None, metadata={'unit': 'float'})
    e_w: np.array = field(default=None, metadata={'unit': 'str'})
    y_offset: np.array = field(default=None, metadata={'unit': 'float'})
    dls: np.array = field(default=None, metadata={'unit': 'float'})
    surface_latitude: np.array = field(default=None, metadata={'unit': 'float'})
    surface_longitude: np.array = field(default=None, metadata={'unit': 'float'})
    surface_x: np.array = field(default=None, metadata={'unit': 'float'})
    surface_y: np.array = field(default=None, metadata={'unit': 'float'})
    x_points: np.array = field(default=None, metadata={'unit': 'float'})
    y_points: np.array = field(default=None, metadata={'unit': 'float'})
    zone_number: np.array = field(default=None, metadata={'unit': 'int'})
    zone_letter: np.array = field(default=None, metadata={'unit': 'str'})
    latitude_points: np.array = field(default=None, metadata={'unit': 'float'})
    longitude_points: np.array = field(default=None, metadata={'unit': 'float'})
