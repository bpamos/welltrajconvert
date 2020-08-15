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
        """
        If surface latitude and longitude are not provided and
        only surface x and surface y are provided the crs_transform must be run.
        This takes in a crs input and transforms the surface x y to surface lat lon,
        in the WGS84 projection space.

        find crs transform input here:
        'https://epsg.io/'

        :parameter:
        crs_in: str
        example input: 'EPSG:4326'

        :return:
        None

        :examples:
        -------
        # with only surface x and y provided you must use the crs transform
        >>> well_dict = {
        ...    "wellId": "well_A",
        ...    "md": [5600.55, 5800.0, 5900.0],
        ...    "inc": [85.03, 89.91, 90.97],
        ...    "azim": [27.59, 26.69, 26.72],
        ...    "surface_x": 759587.9344401711,
        ...    "surface_y": 3311661.864849136
        ... }
        >>> dev_obj = WellboreTrajectory(well_dict) # get wellbore trajectory object
        >>> dev_obj.crs_transform(crs_in='epsg:32638') # requires `crs_transform`
        >>> dev_obj.deviation_survey_obj # view data obj
        # calculates the surface lat and long
        DeviationSurvey(
            wellId='well_A',
            md=array([5600.55, 5800., 5900.]),
            inc=array([85.03, 89.91, 90.97]),
            azim=array([27.59, 26.69, 26.72]),
            surface_latitude=29.90829443997491, surface_longitude=47.68852083021084,
             tvd=None, n_s_deviation=None, e_w_deviation=None, dls=None,
            surface_x=759587.9344401711, surface_y=3311661.864849136,
            x_points=None, y_points=None, zone_number=None, zone_letter=None,
            latitude_points=None, longitude_points=None, isHorizontal=None
        )
        """
        crs_out = "EPSG:4326"

        x = self.deviation_survey_obj.surface_x
        y = self.deviation_survey_obj.surface_y
        self.deviation_survey_obj.surface_latitude, self.deviation_survey_obj.surface_longitude = \
            crs_transformer(crs_out=crs_out, crs_in=crs_in, x=x, y=y)

    def minimum_curvature_algorithm(self):
        """
        Calculate TVD, n_s_deviation, e_w_deviation, and dls values along the wellbore
        using md, inc, and azim

        :parameter:
        -------
        None

        :return:
        -------
        calculated np.array values
        tvd: np.array
        dls: np.array
        e_w_deviation: np.array
        n_s_deviation: np.array

        :examples:
        -------
        >>> well_dict = {
        ...    "wellId": "well_A",
        ...    "md": [5600.55, 5800.0, 5900.0],
        ...    "inc": [85.03, 89.91, 90.97],
        ...    "azim": [27.59, 26.69, 26.72],
        ...    "surface_latitude": 29.90829444,
        ...    "surface_longitude": 47.68852083
        ... }
        >>> dev_obj = WellboreTrajectory(well_dict) # get wellbore trajectory object
        >>> dev_obj.minimum_curvature_algorithm() # calc min curve algo
        >>> dev_obj.deviation_survey_obj # view data obj
        DeviationSurvey(
            wellId='well_A',
            md=array([5600.55, 5800.  , 5900.  ]),
            inc=array([85.03, 89.91, 90.97]),
            azim=array([27.59, 26.69, 26.72]),
            surface_latitude=29.90829444,
            surface_longitude=47.68852083,
            tvd=array([0., 8.80141137, 8.03341735]),
            n_s_deviation=array([0., 177.2584235 , 266.58772113]),
            e_w_deviation=array([0., 90.86066456, 135.79840877]),
            dls=array([0., 2.44319979, 1.05999298]),
            surface_x=None, surface_y=None, x_points=None, y_points=None,
            zone_number=None, zone_letter=None, latitude_points=None, longitude_points=None, isHorizontal=None
        )
        """
        # get md, inc, and azim arrays
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
        -------
        e_w_deviation: np.array
        n_s_deviation: np.array

        required survey data:
        self.surface_latitude: float
        self.surface_longitude: float

        :return:
        -------
        Calculated attributes for lat lon points
        longitude_points: np.array
        latitude_points: np.array
        zone_number: str
        zone_letter: str
        x_points: np.array
        y_points: np.array
        surface_x: np.array
        surface_y: np.array

        :examples:
        -------
        # well dict with surface latitude and longitude
        >>> well_dict = {
        ...    "wellId": "well_A",
        ...    "md": [5600.55, 5800.0, 5900.0],
        ...    "inc": [85.03, 89.91, 90.97],
        ...    "azim": [27.59, 26.69, 26.72],
        ...    "surface_latitude": 29.90829444,
        ...    "surface_longitude": 47.68852083
        ... }
        >>> dev_obj = WellboreTrajectory(well_dict) # get wellbore trajectory object
        >>> dev_obj.minimum_curvature_algorithm() # requires min curve
        >>> dev_obj.calculate_lat_lon_from_deviation_points() # calc lat lon dev points
        >>> dev_obj.deviation_survey_obj # view data obj
        DeviationSurvey(
            wellId='well_A',
            md=array([5600.55, 5800.  , 5900.  ]),
            inc=array([85.03, 89.91, 90.97]),
            azim=array([27.59, 26.69, 26.72]),
            surface_latitude=29.90829444,
            surface_longitude=47.68852083,
            tvd=array([0., 8.80141137, 8.03341735]),
            n_s_deviation=array([0., 177.2584235 , 266.58772113]),
            e_w_deviation=array([0., 90.86066456, 135.79840877]),
            dls=array([0., 2.44319979, 1.05999298]),
            surface_x=759587.9344401711, surface_y=3311661.864849136,
            x_points=array([759587.93444017, 759615.62877073, 759629.32579517]),
            y_points=array([3311661.86484914, 3311715.89321662, 3311743.12078654]),
            zone_number=38, zone_letter='R',
            latitude_points=array([29.90829435, 29.90877556, 29.90901812]),
            longitude_points=array([47.68852365, 47.68882331, 47.68897163]),
            isHorizontal=None
        )

        # with only surface x and y provided
        >>> well_dict = {
        ...    "wellId": "well_A",
        ...    "md": [5600.55, 5800.0, 5900.0],
        ...    "inc": [85.03, 89.91, 90.97],
        ...    "azim": [27.59, 26.69, 26.72],
        ...    "surface_x": 759587.9344401711,
        ...    "surface_y": 3311661.864849136
        ... }
        >>> dev_obj = WellboreTrajectory(well_dict) # get wellbore trajectory object
        >>> dev_obj.crs_transform(crs_in='epsg:32638') # requires `crs_transform`
        >>> dev_obj.minimum_curvature_algorithm() # requires min curve
        >>> dev_obj.calculate_lat_lon_from_deviation_points() # calc lat lon dev points
        >>> dev_obj.deviation_survey_obj # view data obj
        DeviationSurvey(
            wellId='well_A',
            md=array([5600.55, 5800.  , 5900.  ]),
            inc=array([85.03, 89.91, 90.97]),
            azim=array([27.59, 26.69, 26.72]),
            surface_latitude=29.90829443997491, surface_longitude=47.68852083021084,
            tvd=array([0., 8.80141137, 8.03341735]),
            n_s_deviation=array([0., 177.2584235 , 266.58772113]),
            e_w_deviation=array([0., 90.86066456, 135.79840877]),
            dls=array([0., 2.44319979, 1.05999298]),
            surface_x=759587.9344606012, surface_y=3311661.864846832,
            x_points=array([759587.9344606 , 759615.62879116, 759629.3258156 ]),
            y_points=array([3311661.86484683, 3311715.89321431, 3311743.12078423]),
            zone_number=38, zone_letter='R',
            latitude_points=array([29.90829435, 29.90877556, 29.90901812]),
            longitude_points=array([47.68852365, 47.68882331, 47.68897163]),
            isHorizontal=None
        )
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

    # TODO: get the angle value to work in **kwargs
    def calculate_horizontal(self, horizontal_angle: Optional[float] = 88.0):
        """
        calculate if the inclination of the wellbore is in its horizontal section
        If the wellbore inclination is greater than 88 degrees the wellbore is horizontal
        else the well is vertical

        :parameter:
        None

        :return:
        inc_hz:     (np.array)
        """
        inc = self.deviation_survey_obj.inc # get inc points

        # inc greater than 88 deg is horizontal, else vertical
        inc_hz = np.greater(inc, horizontal_angle)
        inc_hz = np.where((inc_hz == True), 'Horizontal', 'Vertical')

        self.deviation_survey_obj.isHorizontal = inc_hz

    def calculate_survey_points(self, **kwargs):
        """
        Run the minimum_curvature_algorithm, calculate_lat_lon_from_deviation_points, and calculate_horizontal
        functions to calculate the wells lat lon points and other attributes from provided md, inc, azim
        and surface lat lon

        :parameter:
        None

        :return:
        survey_points_obj:       (DirectionalSurvey obj)

        :examples:
        -------
        # well dict with surface latitude and longitude
        >>> well_dict = {
        ...    "wellId": "well_A",
        ...    "md": [5600.55, 5800.0, 5900.0],
        ...    "inc": [85.03, 89.91, 90.97],
        ...    "azim": [27.59, 26.69, 26.72],
        ...    "surface_latitude": 29.90829444,
        ...    "surface_longitude": 47.68852083
        ... }
        >>> dev_obj = WellboreTrajectory(well_dict) # get wellbore trajectory object
        >>> dev_obj.calculate_survey_points() # runs through min curve algo, calc lat lon points, and calc horizontal
        >>> dev_obj.deviation_survey_obj # view data obj
        DeviationSurvey(
            wellId='well_A',
            md=array([5600.55, 5800., 5900.  ]),
            inc=array([85.03, 89.91, 90.97]), azim=array([27.59, 26.69, 26.72]),
            surface_latitude=29.90829443997491, surface_longitude=47.68852083021084,
            tvd=array([0., 8.80141137, 8.03341735]),
            n_s_deviation=array([0., 177.2584235 , 266.58772113]),
            e_w_deviation=array([0., 90.86066456, 135.79840877]),
            dls=array([0., 2.44319979, 1.05999298]),
            surface_x=759587.9344606012, surface_y=3311661.864846832,
            x_points=array([759587.9344606 , 759615.62879116, 759629.3258156 ]),
            y_points=array([3311661.86484683, 3311715.89321431, 3311743.12078423]),
            zone_number=38, zone_letter='R',
            latitude_points=array([29.90829435, 29.90877556, 29.90901812]),
            longitude_points=array([47.68852365, 47.68882331, 47.68897163]),
            isHorizontal=array(['Vertical', 'Horizontal', 'Horizontal'], dtype='<U10')
        )

                # with only surface x and y provided
        >>> well_dict = {
        ...    "wellId": "well_A",
        ...    "md": [5600.55, 5800.0, 5900.0],
        ...    "inc": [85.03, 89.91, 90.97],
        ...    "azim": [27.59, 26.69, 26.72],
        ...    "surface_x": 759587.9344401711,
        ...    "surface_y": 3311661.864849136
        ... }
        >>> dev_obj = WellboreTrajectory(well_dict) # get wellbore trajectory object
        >>> dev_obj.crs_transform(crs_in='epsg:32638') # requires `crs_transform`
        >>> dev_obj.calculate_survey_points() # runs through min curve algo, calc lat lon points, and calc horizontal
        >>> dev_obj.deviation_survey_obj # view data obj
        DeviationSurvey(
            wellId='well_A',
            md=array([5600.55, 5800.  , 5900.  ]),
            inc=array([85.03, 89.91, 90.97]),
            azim=array([27.59, 26.69, 26.72]),
            surface_latitude=29.90829443997491, surface_longitude=47.68852083021084,
            tvd=array([0., 8.80141137, 8.03341735]),
            n_s_deviation=array([0., 177.2584235 , 266.58772113]),
            e_w_deviation=array([0., 90.86066456, 135.79840877]),
            dls=array([0., 2.44319979, 1.05999298]),
            surface_x=759587.9344606012, surface_y=3311661.864846832,
            x_points=array([759587.9344606 , 759615.62879116, 759629.3258156 ]),
            y_points=array([3311661.86484683, 3311715.89321431, 3311743.12078423]),
            zone_number=38, zone_letter='R',
            latitude_points=array([29.90829435, 29.90877556, 29.90901812]),
            longitude_points=array([47.68852365, 47.68882331, 47.68897163]),
            isHorizontal=array(['Vertical', 'Horizontal', 'Horizontal'], dtype='<U10')
        )
        """
        for k, v in kwargs.items():
            print(k, v)

        # check if surface lat and long are provided, else, use crs_transform to transform surface x and y
        if self.deviation_survey_obj.surface_latitude is None and self.deviation_survey_obj.surface_longitude is None:
            self.crs_transform(**kwargs)

        self.minimum_curvature_algorithm() # get minimum curvature points

        self.calculate_lat_lon_from_deviation_points() # get lat lon points

        self.calculate_horizontal() # calc horizontal
