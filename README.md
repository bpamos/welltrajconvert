# welltrajconvert

The `welltrajconvert` python package allows the user to take the bare minimum required wellbore survey information and convert that into its latitude and longitude points along the wellbore and a host of other common parameters.

`welltrajconvert` requires the wellId, measured depth, inclination angle, azimuth degrees, surface_latitude, and surface_longitude points to calculate various points along the wellbore using a minimum curvature algorithm.

`welltrajconvert` calculates the following points along the wellbore latitude_points, longitude_points, x_points, y_points, surface_x, surface_y, dogleg severity, tvd, and a categorical array defining if the well is horizontal or not.


The library can take a variety of data inputs ranging from csv, df, and json.


see https://welltrajconvert.readthedocs.io/en/latest/? for complete documentation.



# Installation

Prerequisites: Python 3.7 or later.

It is recommended to install the most recent **stable** release of welltrajconvert from PyPI.

.. code-block:: shell

    $ pip install welltrajconvert


Alternatively, you could install from source code. This will give you the **latest**, but unstable, version of welltrajconvert.

.. code-block:: shell

    $ git clone https://github.com/bpamos/welltrajconvert.git
    $ cd welltrajconvert/
    $ pip install ./
	
## Overview


---


1. Create (and activate) a new environment, named `welltrajconvert` with Python 3.7. If prompted to proceed with the install `(Proceed [y]/n)` type y.

	- __Linux__ or __Mac__: 
	```
	conda create -n welltrajconvert python=3.7
	source activate welltrajconvert
	```
	- __Windows__: 
	```
	conda create --name welltrajconvert python=3.7
	activate welltrajconvert
	```
	
	At this point your command line should look something like: `(welltrajconvert) <User>:welltrajconvert <user>$`. The `(welltrajconvert)` indicates that your environment has been activated, and you can proceed with further package installations.