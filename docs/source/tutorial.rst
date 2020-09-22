Tutorial
========

Getting started
---------------

Before you can use :mod:`welltrajconvert`, you have to import and initialize it::

    from welltrajconvert.wellbore_trajectory import *


Transferring Data
-----------------

The next step is to transfer data into :mod:`welltrajconvert`.
Data formats vary from survey to survey depending on where it is coming from or what vendor is supplying it.
The data could come from a single csv, a csv with multiple wells, from a database via a SQL query, a txt file, ect.

Due to this, the welltrajconvert ensures consistency by only accepting a :py:class:`JSON` document
or a :py:class:`dict` in a specific format.
To get data into this format there are a host of helper functions, see the :mod:`welltrajconvert.DataSource` class.

In this example we will start by importing the data in the required :py:class:`JSON` format,
and the next example we will create the data from a :py:class:`dict`.

Let's import a json.::

    json_path = path/'data/wellbore_survey.json'

Using the :mod:`welltrajconvert.WellboreTrajectory` module, use the `from_json` abstract method
to grab the path and convert its contents into a deviation survey object.
This step will validate if the json contains the correct data for the minimum curvature calculation.::

    # create a wellbore deviation object from the json path
    dev_obj = WellboreTrajectory.from_json(json_path)

If the raw data passes the validation steps it can be viewed here::

    # take a look at the data
    dev_obj.deviation_survey_obj

Let's import the data as a :py:class:`dict`::

    well_dict = {
        "wellId": "well_A",
        "md": [5600.55, 5800.0, 5900.0],
        "inc": [85.03, 89.91, 90.97],
        "azim": [27.59, 26.69, 26.72],
        "surface_latitude": 29.90829444,
        "surface_longitude": 47.68852083
        }

Since we already have the dict object we do not need to call, `from_json`.
Lets just pass the dict directly into :class:`welltrajconvert.WellboreTrajectory`::

    dev_obj = WellboreTrajectory(well_dict) # get wellbore trajectory object
    # take a look at the data
    dev_obj.deviation_survey_obj

Calculate Directional Survey Points
------------------------------------

Once you have imported your data in as a deviation survey object, the rest is simple.
Lets calculate the directional survey metadata following the steps from above.

Here, we are only given input data for wellId, md, inc, azim, and surface latitude and longitude.
The rest of the data is missing and needs to be
calculated with the :class:`welltrajconvert.WellboreTrajectory.calculate_survey_points`::

    # now you can calculate the survey points using a minimum curvature algorithm
    dev_obj.calculate_survey_points()
    # take a look at the data that was just calculated
    dev_obj.deviation_survey_obj

    dev_obj = WellboreTrajectory(well_dict) # get wellbore trajectory object
    # take a look at the data
    dev_obj.deviation_survey_obj

Serialize Data
------------------

Finally you can serialize the data to export and use in a variety of applications.::

    json_ds = dev_obj.serialize()

Advanced Topics
------------------

Calculate Directional Survey Points from Surface X, Y points
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Data does not always come with surface latitude and longitude provided.
Sometimes only surface X, Y points are given.
In the case that only X, Y surface coordinates are provided you can still
calculate the survey points with one additional step.
The user must find the CRS coordinate system and provide that in the calculation.

Let's import the data as a :class:`dict` (notice, surface X, Y are provided instead of lat long)::

    # with only surface x and y provided
    well_dict = {
        "wellId": "well_A",
        "md": [5600.55, 5800.0, 5900.0],
        "inc": [85.03, 89.91, 90.97],
        "azim": [27.59, 26.69, 26.72],
        "surface_x": 759587.9344401711,
        "surface_y": 3311661.864849136
        }

Since we already have the dict object we do not need to call, `from_json`.
Lets just pass the dict directly into :class:`welltrajconvert.WellboreTrajectory`::

    dev_obj = WellboreTrajectory(well_dict) # get wellbore trajectory object
    dev_obj.deviation_survey_obj # take a look at the data

CRS Transform
------------------

Once you have imported your data in as a deviation survey object there is one final step.
Because you do not have the surface latitude and longitude you must provide a :class:`welltrajconvert.WellboreTrajectory.crs_transform()`
This requires you to enter in the EPSG coordinate system for your data. Find your EPSG coordinate system `here <https://epsg.io/>`_.

This takes in a crs input and transforms the surface x y coordinates to surface lat lon in the WGS84 projection space.::

    # example epsg provided
    dev_obj.crs_transform(crs_to='epsg:32638') # requires `crs_transform`


Calculate Directional Survey Points
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After this, follow the same steps as above to calculate the directional survey points::

    dev_obj.calculate_lat_lon_from_deviation_points() # calc lat lon dev points
    # take a look at the data
    dev_obj.deviation_survey_obj


Calculate Horizontal
-------------------------

This is how you calculate the horizontal section. (WIP)

Dealing with Different Data Sources
------------------------------------------

Survey data does not typically come in a dict or json format.
It commonly comes in a tabular format, either from databases via an SQL query or from individual or combined CSVs.
We can handle different data sources by using the :class:`welltrajconvert.DataSource()` class.
Lets jump in and see how it works.

From CSV
------------------

The DataSource module lets you bring in a csv from a csv path or path string using :class:`welltrajconvert.DataSource.from_csv()`.
The user is required to fill in the column name parameters and the module coverts this into a the required :class:`dict` format.
Lets bring in an example::

    my_data = DataSource.from_csv('C:/Users/My/Path/wellpath.csv', wellId_name='wellId',md_name='md',inc_name='inc',azim_name='azim',
             surface_latitude_name='surface_latitude',surface_longitude_name='surface_longitude')
    my_data.data # check out the data

Now the data has been converted into the required :class:`dict` format for the directional survey converter.
Now the user can just follow the steps from above to calculate the survey points.

Calculate the survey points::

    dev_obj = WellboreTrajectory(my_data.data)
    dev_obj.calculate_survey_points()


Serialize the data and view it as a Dataframe::

    json_ds = dev_obj.serialize()
    json_ds_obj = json.loads(json_ds)
    df_min_curve = pd.DataFrame(json_ds_obj)

From Pandas DataFrame:
------------------------

Following a similar format as above, the user can bring in data from a pandas DataFrame.
Just use :class:`welltrajconvert.DataSource.from_df()` and enter in the parameters.::

    my_data = DataSource.from_df(df, wellId_name='wellId',md_name='md',inc_name='inc',azim_name='azim',
             surface_latitude_name='surface_latitude',surface_longitude_name='surface_longitude')
    my_data.data # view the data

Now the data has been converted into the required :class:`dict` format for the directional survey converter.
Now the user can just follow the steps from above to calculate the survey points.

Calculate the survey points::

    dev_obj = WellboreTrajectory(my_data.data)
    dev_obj.calculate_survey_points()

Serialize the data and view it as a Dataframe::

    json_ds = dev_obj.serialize()
    json_ds_obj = json.loads(json_ds)
    df_min_curve = pd.DataFrame(json_ds_obj)

From Dictionary:
------------------

Of course, the user can bring data in from a dictionary format as well using the :class:`welltrajconvert.DataSource.from_dictionary()` method.::

    my_data = DataSource.from_dictionary(json_data)
    # calculate the survey points
    dev_obj = WellboreTrajectory(my_data.data
    dev_obj.calculate_survey_points()
    # serialze and view as a dataframe.
    json_ds = dev_obj.serialize()
    json_ds_obj = json.loads(json_ds)
    df_min_curve = pd.DataFrame(json_ds_obj)

