# welltrajconvert

The `welltrajconvert` is a Python package that allows a user to take the bare minimum required
wellbore survey information and return it's directional survey points including its latitude, longitude, TVD, XY offset,
and UTM points.

`welltrajconvert` requires only the wellId, measured depth, inclination angle, azimuth degrees, surface latitude,
and surface longitude points or surface UTM XY and associated CRS to calculate its survey points using a minimum curvature algorithm.

`welltrajconvert` calculates the following points along the wellbore: latitude_points, longitude_points, x_points, y_points, surface_x, surface_y, dogleg severity, tvd, e_w_deviaiton, n_s_deviation, zone_number, zone_letter, and isHorizontal, a categorical array defining if the well is horizontal or not.


The package can take a variety of data inputs ranging from csv, df, and json.


see https://welltrajconvert.readthedocs.io/en/latest/ for complete documentation.



# Installation

Prerequisites: Python 3.7 or later.

It is recommended to install the most recent **stable** release of welltrajconvert from PyPI.


    $ pip install welltrajconvert


Alternatively, you could install from source code. This will give you the **latest**, but unstable, version of welltrajconvert.


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
