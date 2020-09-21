Welcome to welltrajconvert's documentation!
========================================================

`welltrajconvert` gives you and easy way to convert the numerous different styles of wellbore directional surveys often delivered by service companies into a standard format with all the metadata a user is typically interested in. Using the bare minimum information given the welltrajconvert uses a minimum curvature algorithm to calculate survey points along the wellbore so the user can have all the data they need to perform their analysis. Why should you use the welltrajconvert?

* You have a single survey with only the MD, INC, AZIM, and surface latitude and longitude and need additional metadata.

* You have a single survey with only the MD, INC, AZIM, and surface x and y coordinates and need additional metadata.

* You want to display your wellbore trajectory geospatially using latitude and longitude points along the wellbore.

* Helpful Documentation. You're looking at it. ;)

Here's an example, to give you an impression::

   from src.wellbore_trajectory import *
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

Output:

.. image:: _static/image/df_example_p1.png

output continued...

.. image:: _static/image/df_example_p2.png

(This example is :file:`examples/MAKE_EXAMPLE_FILE.py` in the welltrajconvert
source distribution.)

On the surface it looks quite simple. Behind the scenes there is a lot more interesting stuff going on:

* Bring data in and convert it into a dataclass object.

* Validate the data conforms to proper directional survey structure for the minimum curvature algorithm

* Check if surface latitude and longitude or surface x and y are provided.

* Calculate horizontal section based on default or user input angle.

* Deserialize data into a format that can be used in a variety of applications.

* Ability to take in a variety of data sources and formats and compute meta data.

Curious? Let’s get started.

Contents
=========

.. toctree::
    :maxdepth: 2

    install
    tutorial
    notebook/GettingStarted.ipynb
    api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

