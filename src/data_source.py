from src.utils import *


class DataSource:
    """
    Accept different data types and transforms them into the wellbore trajectory data format.
    """

    def __init__(self, data=None):
        """
        Accepts various data sources and converts them into format for wellbore trajectory class.
        pass in csv path, path or string
        df
        dict
        json string

        :Parameters:


        :Return:
        data object
        """

        self.data = data

    # TODO: is this needed?
    @classmethod
    def from_json(cls, json_obj):
        """
        Take json string and turn it into the data object used in `WellTrajectory`

        :Parameters:
        json string

        :Return:
        data object
        """
        # serialize
        json_obj = json.loads(json_obj)
        res = cls(data=json_obj)
        return res

    # TODO: add the key names so the user can choose?
    @classmethod
    def from_dictionary(cls, dict_obj):
        """
        serialize dict object to string

        :Parameters:
        dict object

        :Return:
        str used in `from_json`
        """

        json_string = json.dumps(dict_obj)  # serialize
        return cls.from_json(json_string)

    @classmethod
    def from_df(cls, df, wellId_name: str = None, md_name: str = None,
                inc_name: str = None, azim_name: str = None,
                surface_latitude_name: Optional[str] = None,
                surface_longitude_name: Optional[str] = None,
                surface_x_name: Optional[str] = None,
                surface_y_name: Optional[str] = None):
        """
        convert a well survey df into dict format used in `WellboreTrajectory`
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
        dict used in `from_dictionary`
        """
        # if no column names are specified use 0:5 for dir survey obj
        surface_latitude_name = if_none(surface_latitude_name, None)
        surface_longitude_name = if_none(surface_longitude_name, None)
        surface_x_name = if_none(surface_x_name, None)
        surface_y_name = if_none(surface_y_name, None)

        cols = list(df.columns)
        # check to make sure no columns have NaN values
        inputs = df.iloc[:, df_names_to_idx(cols, df)]
        assert not inputs.isna().any().any(), f"You have NaN values in column(s) {cols} of your dataframe, please fix it."

        if surface_latitude_name is not None and surface_longitude_name is not None:
            dict_obj = dict(wellId=str(df[wellId_name][0]),
                            md=list(df[md_name]),
                            inc=list(df[inc_name]),
                            azim=list(df[azim_name]),
                            surface_latitude=float(df[surface_latitude_name][0]),
                            surface_longitude=float(df[surface_longitude_name][0]))

        if surface_x_name is not None and surface_y_name is not None:
            dict_obj = dict(wellId=str(df[wellId_name][0]),
                            md=list(df[md_name]),
                            inc=list(df[inc_name]),
                            azim=list(df[azim_name]),
                            surface_x=float(df[surface_x_name][0]),
                            surface_y=float(df[surface_y_name][0]))

        return cls.from_dictionary(dict_obj)

    @classmethod
    def from_csv(cls, path: PathOrStr, wellId_name: Optional[str] = None, md_name: Optional[str] = None,
                 inc_name: Optional[str] = None, azim_name: Optional[str] = None,
                 surface_latitude_name: Optional[str] = None,
                 surface_longitude_name: Optional[str] = None,
                 surface_x_name: Optional[str] = None,
                 surface_y_name: Optional[str] = None):
        """
        convert a csv path into df with required column information.
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
        df used in `from_df`
        wellId_name (str)
        md_name (str)
        inc_name (str)
        azim_name (str)
        surface_latitude_name (str)
        surface_longitude_name (str)
        or
        surface_x_name (str)
        surface_y_name (str)
        """

        df = pd.read_csv(path, sep=',')

        return cls.from_df(df, wellId_name=wellId_name, md_name=md_name,
                           inc_name=inc_name, azim_name=azim_name,
                           surface_latitude_name=surface_latitude_name,
                           surface_longitude_name=surface_longitude_name,
                           surface_x_name=surface_x_name,
                           surface_y_name=surface_y_name)
