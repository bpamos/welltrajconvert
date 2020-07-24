from src.calculable_object import *


class WellboreTrajectory(CalculableObject):

    def __init__(self, deviation_survey_obj):
        """
        DirectionalSurvey object with a wells directional survey info

        Attributes:
        directional_survey_points (Dataclass Object) DataObject object
        """

        self.deviation_survey_obj = DeviationSurvey(**deviation_survey_obj)

    # TODO: not sure this is the right implementation, should this be somewhere else?
    # using self here is confusing, I dont think it is correct.
    def deserialize(self):
        with open(self) as json_file:
            data = json.load(json_file)
        json_file.close()
        return data

    def calculate_survey_points(self):
        super().calculate_survey_points()

    def get_survey_df(self):
        """
        Convert survey object to dataframe

        :parameter:
        None

        :return:
        survey_df:      (dataframe)

        """

        survey_df = pd.DataFrame({'wellId': self.deviation_survey_obj.wellId,
                                  'md': self.deviation_survey_obj.md,
                                  'inc': self.deviation_survey_obj.inc,
                                  'azim': self.deviation_survey_obj.azim,
                                  'tvd': self.deviation_survey_obj.tvd,
                                  'e_w_deviation': self.deviation_survey_obj.e_w_deviation,
                                  'n_s_deviation': self.deviation_survey_obj.n_s_deviation,
                                  'dls': self.deviation_survey_obj.dls,
                                  'surface_latitude': self.deviation_survey_obj.surface_latitude,
                                  'surface_longitude': self.deviation_survey_obj.surface_longitude,
                                  'longitude_points': self.deviation_survey_obj.longitude_points,
                                  'latitude_points': self.deviation_survey_obj.latitude_points,
                                  'zone_number': self.deviation_survey_obj.zone_number,
                                  'zone_letter': self.deviation_survey_obj.zone_letter,
                                  'x_points': self.deviation_survey_obj.x_points,
                                  'y_points': self.deviation_survey_obj.y_points,
                                  'surface_x': self.deviation_survey_obj.surface_x,
                                  'surface_y': self.deviation_survey_obj.surface_y,
                                  'isHorizontal': self.deviation_survey_obj.isHorizontal
                                  })

        return survey_df