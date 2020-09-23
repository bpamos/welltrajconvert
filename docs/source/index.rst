welltrajconvert Overview
========================================================

:mod:`welltrajconvert` is a Python package that allows a user to take the bare minimum required
wellbore survey information and return it's directional survey points including its latitude, longitude, TVD, XY offset,
and UTM points. The package requires only the wellId, measured depth, inclination angle, azimuth degrees, surface latitude,
and surface longitude points or surface UTM XY and associated CRS to calculate its survey points using a minimum curvature algorithm.

Why should you use :mod:`welltrajconvert`?

* You want to display your wellbore trajectory geospatially using latitude and longitude points along the wellbore.

* You have a single survey with only the MD, INC, AZIM, and surface latitude and longitude and need comprehensive survey points.

* You have a single survey with only the MD, INC, AZIM, and surface X and Y coordinates and need comprehensive survey points.

* You have multiple surveys and want a standardized comprehensive output with data typically required for additional analytics.

Here's an example, to give you an impression:

**Input**::

   # import wellbore_trajectory from welltrajconvert
   from welltrajconvert.wellbore_trajectory import *

   # example dict
   well_dict = {
   "wellId": "well_A",
   "md": [5600.55, 5800.0, 5900.0],
   "inc": [85.03, 89.91, 90.97],
   "azim": [27.59, 26.69, 26.72],
   "surface_latitude": 29.90829444,
   "surface_longitude": 47.68852083
   }

   dev_obj = WellboreTrajectory(well_dict) # get wellbore trajectory object
   dev_obj.calculate_survey_points() # runs through min curve algo, calc lat lon points, and calc horizontal
   json_ds = dev_obj.serialize() # serialize to json
   json_ds_obj = json.loads(json_ds)
   df = pd.DataFrame(json_ds_obj) # convert dict to dataframe
   df.head() # display dataframe

**Output**::

       wellId       md    inc   azim       tvd  e_w_deviation  n_s_deviation        dls  surface_latitude  surface_longitude  longitude_points   latitude_points  zone_number zone_letter       x_points      y_points      surface_x     surface_y isHorizontal
    0  well_A  5600.55  85.03  27.59  0.000000       0.000000       0.000000   0.000000         29.908294          47.688521         47.688521         29.908294           38           R  759587.934440  3.311662e+06   759587.93444  3.311662e+06     Vertical
    1  well_A  5800.00  89.91  26.69  8.801411      90.860665     177.258423   2.443200         29.908294          47.688521         47.688820         29.908776           38           R  759615.628771  3.311716e+06   759587.93444  3.311662e+06   Horizontal
    2  well_A  5900.00  90.97  26.72  8.033417     135.798409     266.587721   1.059993         29.908294          47.688521         47.688969         29.909018           38           R  759629.325795  3.311743e+06   759587.93444  3.311662e+06   Horizontal


On the surface it looks quite simple. Behind the scenes there is a lot more interesting stuff going on:

* Bringing data in and converting it into a dataclass object.

* Validate that the data conforms to proper directional survey structure for the minimum curvature algorithm.

* Check if the surface latitude and longitude or surface X and Y are provided.

* Calculate horizontal section when inclination is >= 88 degrees.

* Serialize and deserialize data into a format that can be used in a variety of applications.

* Ability to take in a variety of data sources and formats and compute survey data.

Curious? Let’s get started.

Contents
=========

.. toctree::
    :maxdepth: 3

    install
    tutorial
    notebook/Getting Started.ipynb
    notebook/Getting Started with Data Sources.ipynb
    api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

