from dataclasses import dataclass, field
import numpy as np

@dataclass
class DirectionalSurvey:
    """
    Dataclass for Directional Survey Points, takes a list of dictionaries and converts them into np.arrays
    The data class accepts common directional survey params, some are required, depending on which params
    are provided the calculation choose the correct method for directional survey conversion.
    Intended to be run per well.

    Args:
    wellId (required):
    md (required): measured depth
    inc (required): inclination angle
    azim (required): azimuth degrees
    tvd: true vertical depth
    n_s_deviation: north south deviation (all postitive)
    n_s: north or south id (used to convert n_s_deviation to positive or negative)
    x_offset: n_s_deviation with its north or south id conversion
    e_w_deviation: east west deviation (all postitive)
    e_w: east or west id (used to convert e_w_devitaion to positive or negative)
    y_offset: e_w_devitaion with its east or west id conversion
    surface_latitude: surface hole latitude
    surface_longitude: surface hole longitude
    surface_x
    surface_y
    x_points: 
    y_points: 
    zone_number: 
    zone_letter: 
    latitude_points: 
    longitude_points: 

    Returns:
    dataclass Directional Survey object
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