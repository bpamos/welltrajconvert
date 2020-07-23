# directional-survey-converter

The directional-survey-converter library allows the user to take the bare minimum required wellbore survey information and convert that into its latitude and longitude points along the wellbore and a host of other common parameters.
The directional-survey-converter requires the wellId, measured depth, inclination angle, azimuth degrees, surface_latitude, and surface_longitude points to calculate various points along the wellbore using a minimum curvature algorithm.
The directional-survey-converter calculates the following points along the wellbore latitude_points, longitude_points, x_points, y_points, surface_x, surface_y, dogleg severity, tvd, and a categorical array defining if the well is horizontal or not.


The library can take a variety of data inputs ranging from csv, df, and json.



# Installation

## Pip Install



## Overview


---


1. Create (and activate) a new environment, named `directional-survey-converter` with Python 3.6. If prompted to proceed with the install `(Proceed [y]/n)` type y.

	- __Linux__ or __Mac__: 
	```
	conda create -n dir-survey python=3.6
	source activate dir-survey
	```
	- __Windows__: 
	```
	conda create --name dir-survey python=3.6
	activate dir-survey
	```
	
	At this point your command line should look something like: `(directional-survey-converter) <User>:directional-survey-converter <user>$`. The `(directional-survey-converter)` indicates that your environment has been activated, and you can proceed with further package installations.