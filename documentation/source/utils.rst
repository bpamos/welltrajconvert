.. _reference-doc:

Built-in Utilities
==================

.. module:: directional-survey-converter

Data Object
--------------------

A abstract base class to work with subclasses `DeviationSurvey` and `CalculableObject`.

.. class:: DataObject

    methods in `DataObject`

    .. method:: from_json()
    .. method:: validate()
    .. method:: deserialize()
    .. method:: serialize()

Deviation Survey
--------------------

Dataclass for Directional Survey Points takes a single `DataObject` and validates and serializes it.
Then converts it into a Dataclass object of Deviation Survey points, ensuring that all the correct data types
are present for later calculations.

Calculable Object
--------------------

DirectionalSurvey object with a wells directional survey info

Attributes:
directional_survey_points (Dataclass Object) DataObject object


Wellbore Trajectory
--------------------

DirectionalSurvey object with a wells directional survey info

Attributes:
directional_survey_points (Dataclass Object) DataObject object


.. class:: WellboreTrajectory

    .. method:: crs_transform()
    .. method:: minimum_curvature_algorithm()
    .. method:: calculate_lat_lon_from_deviation_points()
    .. method:: calculate_horizontal()
    .. method:: calculate_survey_points()

Data Source
--------------------

Accept different data types and transforms them into the wellbore trajectory data format.

.. class:: DataSource

    .. method:: from_json(cls, json_obj)
    .. method:: from_dictionary(cls, dict_obj)
    .. method:: from_df(cls, df, wellId_name: str = None, md_name: str = None, inc_name: str = None, azim_name: str = None, surface_latitude_name: Optional[str] = None, surface_longitude_name: Optional[str] = None, surface_x_name: Optional[str] = None, surface_y_name: Optional[str] = None)
    .. method:: from_csv(cls, path: PathOrStr, wellId_name: Optional[str] = None, md_name: Optional[str] = None, inc_name: Optional[str] = None, azim_name: Optional[str] = None, surface_latitude_name: Optional[str] = None, surface_longitude_name: Optional[str] = None, surface_x_name: Optional[str] = None, surface_y_name: Optional[str] = None)

