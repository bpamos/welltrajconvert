Tutorial
========

Getting started
---------------

Before you can use directional-survey-converter, you have to import and initialize it::

    from src.wellbore_trajectory import *


Transferring Data
-----------------

The next step is to transfer data into the directional-survey-converter.
Data formats vary from suvery to survey depending on where it is coming from.
The data could come from a single csv, a csv with multiple wells, from a database via an SQL query, txt file, ect.
Due to this fact, the directional-survey-converter accepts a :class:`json` document or a :class:`dict` in a specific format.
To get data into this format there are a host of helper functions, see here `LINK`.
In this example we will start with the data in the proper :class:`json` format, follwed by a :class:`dict`.
Let's import a json.::

    json_path = path/'data/wellbore_survey.json'

Using the WellboreTrajectory class, use `from_json` to take the path and convert it to a deviation survey object. This step will validate if the json contains the correct data for the minimum curvature calculation.::

    # create a wellbore deviation object from the json path
    dev_obj = WellboreTrajectory.from_json(json_path)

If the raw data passes the validation steps it can be viewed here::

    # take a look at the data
    dev_obj.deviation_survey_obj

Let's import a :class:`dict`::

    well_dict = {
        "wellId": "well_A",
        "md": [5600.55, 5800.0, 5900.0],
        "inc": [85.03, 89.91, 90.97],
        "azim": [27.59, 26.69, 26.72],
        "surface_latitude": 29.90829444,
        "surface_longitude": 47.68852083
        }
Since we already have the dict object we do not need to call, `from_json`
Lets just pass the dict directly into WellboreTrajectory()::

    dev_obj = WellboreTrajectory(well_dict) # get wellbore trajectory object
    # take a look at the data
    dev_obj.deviation_survey_obj

Calculate Directional Survey Points
------------------
Once you have imported your data in, the rest is simple.
Lets calculate the directional survey metadata following the steps from above.
Here, we are only given input data for wellId, md, inc, azim, and surface latitude and longitude.
The rest of the data is missing and needs to be calculated with the :class:`WellboreTrajectory.calculate_survey_points()`::::

    # now you can calculate the survey points using a minimum curvature algorithm
    dev_obj.calculate_survey_points()
    # take a look at the data that was just calculated
    dev_obj.deviation_survey_obj

    dev_obj = WellboreTrajectory(well_dict) # get wellbore trajectory object
    # take a look at the data
    dev_obj.deviation_survey_obj

Serialize Data
------------------
Finally you can serialize the data to use in a variety of applications.::

    json_ds = dev_obj.serialize()
