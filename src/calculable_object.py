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

    def serialize(self):
        super().serialize()

    @classmethod
    def from_json(cls, path: PathOrStr):

        with open(path) as json_file:
            json_data = json.load(json_file)
        json_file.close()

        res = cls(data=json_data)
        return res

    def deserialize(self):
        """
        Convert survey object to deserialized json

        :parameter:
        None

        :return:
        json:      (json object)

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

        json_string = json.dumps(json_obj)

        return json_string
