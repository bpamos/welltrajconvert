from src.deviation_survey import *


class CalculableObject(DataObject):

    def __init__(self, deviation_survey_obj, **kwargs):
        """
        DirectionalSurvey object with a wells directional survey info

        Attributes:
        directional_survey_points (Dataclass Object) DataObject object
        """

        self.deviation_survey_obj = deviation_survey_obj

    def validate(self):
        super().validate()

    def deserialize(self):
        super().deserialize()

    @classmethod
    def from_json(cls, path: PathOrStr):
        """
        Pass in a json path, either a string or a Path lib path and convert to a WellboreTrajectory data obj

        :param:
        -------
         path: PathOrStr

        :return:
        -------
        deviation_survey_obj: Obj

        :examples:
        -------
        # accepts path or string
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
        """

        with open(path) as json_file:
            json_data = json.load(json_file)
        json_file.close()

        res = cls(data=json_data)  # converts json data
        return res

    def serialize(self):
        """
        Convert survey object to serialized json

        :parameter:
        -------
        None

        :return:
        -------
        json: str

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
        """

        json_obj = dict(wellId=str(self.deviation_survey_obj.wellId),
                        md=list(self.deviation_survey_obj.md),
                        inc=list(self.deviation_survey_obj.inc),
                        azim=list(self.deviation_survey_obj.azim),
                        tvd=list(self.deviation_survey_obj.tvd),
                        e_w_deviation=list(self.deviation_survey_obj.e_w_deviation),
                        n_s_deviation=list(self.deviation_survey_obj.n_s_deviation),
                        dls=list(self.deviation_survey_obj.dls),
                        surface_latitude=float(self.deviation_survey_obj.surface_latitude),
                        surface_longitude=float(self.deviation_survey_obj.surface_longitude),
                        longitude_points=list(self.deviation_survey_obj.longitude_points),
                        latitude_points=list(self.deviation_survey_obj.latitude_points),
                        zone_number=int(self.deviation_survey_obj.zone_number),
                        zone_letter=str(self.deviation_survey_obj.zone_letter),
                        x_points=list(self.deviation_survey_obj.x_points),
                        y_points=list(self.deviation_survey_obj.y_points),
                        surface_x=float(self.deviation_survey_obj.surface_x),
                        surface_y=float(self.deviation_survey_obj.surface_y),
                        isHorizontal=list(self.deviation_survey_obj.isHorizontal))

        json_string = json.dumps(json_obj)  # converts a data object into a json string.

        return json_string
