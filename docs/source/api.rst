.. _reference-doc:

API
==================

This part of the documentation covers all the classes and methods in the directional-survey-converter.

.. module:: directional-survey-converter

Data Object
--------------------

.. class:: DataObject

    A abstract base class to work with subclasses `DeviationSurvey` and `CalculableObject`.

    .. method:: from_json()
    .. method:: validate()
    .. method:: deserialize()
    .. method:: serialize()

Deviation Survey
--------------------

.. class:: DeviationSurvey

    Dataclass for Directional Survey Points takes a single `DataObject` and validates and serializes it.
    Then converts it into a Dataclass object of Deviation Survey points, ensuring that all the correct data types
    are present for later calculations.

    **Parameters:**
        * **wellId:** - (required) Unique well identification id
        * **md:** - (required) measured depth  is the actual depth of the hole drilled to any point along the wellbore or to total depth, as measured from the surface location
        * **inc:** - (required) inclination angle, the angular measurement that the borehole deviates from vertical.
        * **azim:** - (required) azimuth degrees, the hole direction is measured in degrees (0 to 360°)
        * **surface_latitude:** - (required) surface hole latitude
        * **surface_longitude:** - (required) surface hole longitude
        * **tvd:** - true vertical depth from surface to the survey point.
        * **n_s_deviation:** - north south deviation for each point in the wellbore path.
        * **e_w_deviation:** - east west deviation for each point in the wellbore path.
        * **dls:** - Dogleg severity is a measure of the change in direction of a wellbore over a defined length, measured in degrees per 100 feet of length.
        * **surface_x:** - Surface Easting component of the UTM coordinate
        * **surface_y:** - Surface Northing component of the UTM coordinate
        * **x_points:** - Easting component of the UTM coordinate
        * **y_points:** - Northing component of the UTM coordinate
        * **zone_number:** - Zone number of the UTM coordinate
        * **zone_letter:** - Zone letter of the UTM coordinate
        * **latitude_points:** - The latitude value of a location in the borehole. A positive value denotes north. Angle subtended with equatorial plane by a perpendicular from a point on the surface of a spheriod.
        * **longitude_points:** - The longitude value of a location in a borehole. A positive value denotes east. Angle measured about the spheroid axis from a local prime meridian to the meridian through the point.
        * **isHorizontal:** - Array of strings, Vertical Or Horizontal depending on Inclination angle point

    **Returns:**
        * **dataclass obj:** - Dataclass DirectionalSurvey object

    .. method:: from_json()
    .. method:: serialize()
    .. method:: validate()

        validate different parameters to ensure that the data in the DataObject
        will work with the directional survey functions

    .. function:: validate_array_length()

        validate the length of the array, ensure md, inc, and azim are equal lengths

    .. function:: validate_array_sign()

        validate md and inc are not negative

    .. function:: validate_lat_long_range()

        validate that the surface lat and long are between the acceptable ranges


    .. function:: validate_wellId()

        validate that wellId is a string, it needs to be a single wellId value not a list or array of wellIds

    .. function:: validate_array_monotonic()

        check if array is monotonically increasing, always increasing of staying the same

    .. method:: deserialize()

        convert dict values to their proper deserialized dict values
        converts lists to np.arrays if not None
        converts value to float if not None
        converts value to int if not None
        converts value to str if not None

    .. method:: __post_init__()

        validate all data,
        serialized all validated data,
        look in all fields and types,
        if type is None pass,
        else if type given doesnt match dataclass type raise error

Calculable Object
--------------------

.. class:: CalculableObject

    DirectionalSurvey object with a wells directional survey info

    .. attribute:: deviation_survey_obj

        Attributes:
        directional_survey_points (Dataclass Object) DataObject object

    .. method:: from_json(cls, path: PathOrStr)

        Pass in a json path, either a string or a Path lib path and convert to a WellboreTrajectory data obj::

            >>> json_path = path/'data/example.json' # path object
            # alternative:
            >>> json_path = 'C:/Users/data/example.json' # str
            >>> dev_obj = WellboreTrajectory.from_json(json_path) # read in json path and create data obj
            >>> dev_obj.data # view raw json
            {'wellId': 'well_A','md': [5600.55, 5800.0, 5900.0],'inc': [85.03, 89.91, 90.97],
             'azim': [27.59, 26.69, 26.72],'surface_latitude': 29.90829444,'surface_longitude': 47.68852083}
            >>> dev_obj.deviation_survey_obj # view data obj results
            DeviationSurvey(
                wellId='well_A', md=array([5600.55,5800., 5900.]), inc=array([85.03, 89.91, 90.97]),
                azim=array([27.59, 26.69, 26.72]), surface_latitude=29.90829444, surface_longitude=47.68852083,
                tvd=None, n_s_deviation=None, e_w_deviation=None, dls=None, surface_x=None, surface_y=None,
                x_points=None, y_points=None, zone_number=None, zone_letter=None, latitude_points=None,
                longitude_points=None, isHorizontal=None
            )

    .. method:: serialize()

        Convert survey object to serialized json::

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
            >>> dev_obj.serialize() # convert data object to a serialized json string
            '{"wellId": "well_A", "md": [5600.55, 5800.0, 5900.0], "inc": [85.03, 89.91, 90.97],
            "azim": [27.59, 26.69, 26.72], "tvd": [0.0, 8.801411366548953, 8.033417349071017],
            "e_w_deviation": [0.0, 90.86066455861472, 135.79840877475],
            "n_s_deviation": [0.0, 177.2584234997277, 266.5877211334688],
            "dls": [0.0, 2.4431997863679826, 1.0599929804526975],
            "surface_latitude": 29.90829444, "surface_longitude": 47.68852083,
            "longitude_points": [47.6885236512062, 47.68882330644181, 47.688971633323014],
            "latitude_points": [29.90829435014479, 29.908775557209452, 29.90901811572951],
            "zone_number": 38, "zone_letter": "R",
            "x_points": [759587.9344401711, 759615.6287707286, 759629.3257951656],
            "y_points": [3311661.864849136, 3311715.893216619, 3311743.120786538],
            "surface_x": 759587.9344401711, "surface_y": 3311661.864849136,
            "isHorizontal": ["Vertical", "Horizontal", "Horizontal"]}'

Wellbore Trajectory
--------------------

.. class:: WellboreTrajectory

    DirectionalSurvey object with a wells directional survey info

    .. attribute:: data
    .. attribute:: deviation_survey_obj

        Attributes:
        directional_survey_points (Dataclass Object) DataObject object

    .. method:: crs_transform()

        If surface x and y are provied instead of surface latitude and longitude then
        the crs_transform needs to be run.
        This takes in a crs input and transforms the surface x y to surface lat lon,
        in the WGS84 projection space.::

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
            >>> dev_obj.crs_transform(crs_to='epsg:32638') # requires `crs_transform`
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

    .. method:: minimum_curvature_algorithm()

        Calculate TVD, n_s_deviation, e_w_deviation, and dls values along the wellbore
        using md, inc, and azim arrays::

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

    .. method:: calculate_lat_lon_from_deviation_points()

        get latitude and longitude points along the wellbore using the minimum curvature algorithm generated values
        for the ns and ew deviations.::

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

        Or with only surface x and y provided::

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
            >>> dev_obj.crs_transform(crs_to='epsg:32638') # requires `crs_transform`
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


    .. method:: calculate_horizontal()

        calculate if the inclination of the wellbore is in its horizontal section.
        If the wellbore inclination is greater than 88 degrees then wellbore is horizontal
        else the well is vertical.


    .. method:: calculate_survey_points()

        Run the minimum_curvature_algorithm, calculate_lat_lon_from_deviation_points, and calculate_horizontal
        methods to calculate the wells lat lon points and other attributes from provided md, inc, azim
        and surface lat lon or surface x y.::

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

        Or with only surface x and y provided::

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
            >>> dev_obj.crs_transform(crs_to='epsg:32638') # requires `crs_transform`
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

Data Source
--------------------

.. class:: DataSource

    .. attribute:: data

        Accept different data types and transforms them into the wellbore trajectory data format.

    .. method:: from_json(cls, json_obj)

        Take json string and turn it into the data object used in `WellTrajectory`

    .. method:: from_dictionary(cls, dict_obj)

        serialize dict object to string

    .. method:: from_df(cls, df, wellId_name: str = None, md_name: str = None, inc_name: str = None, azim_name: str = None, surface_latitude_name: Optional[str] = None, surface_longitude_name: Optional[str] = None, surface_x_name: Optional[str] = None, surface_y_name: Optional[str] = None)

        convert a well survey df into dict format used in `WellboreTrajectory`
        User must specify column names for wellId, md, inc, azim, and either both
        surface_latitude, surface_longitude, or both surface_x, surface_y


    .. method:: from_csv(cls, path: PathOrStr, wellId_name: Optional[str] = None, md_name: Optional[str] = None, inc_name: Optional[str] = None, azim_name: Optional[str] = None, surface_latitude_name: Optional[str] = None, surface_longitude_name: Optional[str] = None, surface_x_name: Optional[str] = None, surface_y_name: Optional[str] = None)

        convert a csv path into df with required column information.
        User must specify column names for wellId, md, inc, azim, and either both
        surface_latitude, surface_longitude, or both surface_x, surface_y
