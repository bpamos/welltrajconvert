from src.calculable_object import *
from src.base import *


class WellboreTrajectory(CalculableObject):

    def __init__(self, data=None):
        """
        DirectionalSurvey object with a wells directional survey info

        Attributes:
        directional_survey_points (Dataclass Object) DataObject object
        """

        self.data = data
        self.deviation_survey_obj = DeviationSurvey(**self.data)

    @classmethod
    def from_json(cls, path: PathOrStr):

        with open(path) as json_file:
            json_data = json.load(json_file)
        json_file.close()

        res = cls(data=json_data)
        return res

    @classmethod
    def from_df(cls, df, wellId_name: str = None, md_name: str = None,
                inc_name: str = None, azim_name: str = None,
                surface_latitude_name: Optional[str] = None,
                surface_longitude_name: Optional[str] = None,
                surface_x_name: Optional[str] = None,
                surface_y_name: Optional[str] = None):
        """
        convert a well survey df into a list of dicts format used in `WellboreTrajectory`
        User must specify column names for wellId, md, inc, azim, and either both
        surface_latitude, surface_longitude, or both surface_x, surface_y

        :Parameters:
        df
        wellId_name
        md_name
        inc_name
        azim_name
        surface_latitude_name
        surface_longitude_name
        surface_x_name
        surface_y_name

        :Return:
        list of dicts

        """
        # if no column names are specified use 0:5 for dir survey obj
        surface_latitude_name = if_none(surface_latitude_name, None)
        surface_longitude_name = if_none(surface_longitude_name, None)
        surface_x_name = if_none(surface_x_name, None)
        surface_y_name = if_none(surface_y_name, None)

        cols = list(df.columns)
        # check to make sure no columns have NaN values
        inputs = df.iloc[:,df_names_to_idx(cols, df)]
        assert not inputs.isna().any().any(), f"You have NaN values in column(s) {cols} of your dataframe, please fix it."

        if surface_latitude_name is not None and surface_longitude_name is not None:
            dataclass_obj = dict(wellId=df[wellId_name][0],
                                 md=np.array(df[md_name]),
                                 inc=np.array(df[inc_name]),
                                 azim=np.array(df[azim_name]),
                                 surface_latitude=df[surface_latitude_name][0],
                                 surface_longitude=df[surface_longitude_name][0])

        if surface_x_name is not None and surface_y_name is not None:
            dataclass_obj = dict(wellId=df[wellId_name][0],
                                 md=np.array(df[md_name]),
                                 inc=np.array(df[inc_name]),
                                 azim=np.array(df[azim_name]),
                                 surface_x=df[surface_x_name][0],
                                 surface_y=df[surface_y_name][0])

        res = cls(data=dataclass_obj)
        return res

    @classmethod
    def from_csv(cls, path: PathOrStr, wellId_name: Optional[str] = None, md_name: Optional[str] = None,
                 inc_name: Optional[str] = None, azim_name: Optional[str] = None,
                 surface_latitude_name: Optional[str] = None,
                 surface_longitude_name: Optional[str] = None,
                 surface_x_name: Optional[str] = None,
                 surface_y_name: Optional[str] = None):

        df = pd.read_csv(path, sep=',')

        return cls.from_df(df, wellId_name=wellId_name, md_name=md_name,
                           inc_name=inc_name, azim_name=azim_name,
                           surface_latitude_name=surface_latitude_name,
                           surface_longitude_name=surface_longitude_name,
                           surface_x_name=surface_x_name,
                           surface_y_name=surface_y_name)

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