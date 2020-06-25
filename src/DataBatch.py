from src.core import *
from src.utils import *
from src.dataclass import *

class DataBatch:

    def __init__(self, data):
        """


        :param directional_survey_data:
        """

        self.data = data

    def from_df(self: DataFrame, wellId_name: Optional[str] = None, md_name: Optional[str] = None,
                inc_name: Optional[str] = None, azim_name: Optional[str] = None,
                surface_latitude_name: Optional[str] = None,
                surface_longitude_name: Optional[str] = None) -> 'DirectionalSurveyObj':
        """Create a `dataclass_obj` suitable for `DirectionalSurvey()` from a dataframe.

        Params:
        df: Dataframe with well data from single well and all data columns.

        Return:
        dataclass_obj

        """
        df = self.data

        # if no column names are specified use 0:5 for dir survey obj
        wellId_name = ifnone(wellId_name, df.columns[0])
        md_name = ifnone(md_name, df.columns[1])
        inc_name = ifnone(inc_name, df.columns[2])
        azim_name = ifnone(azim_name, df.columns[3])
        surface_latitude_name = ifnone(surface_latitude_name, df.columns[4])
        surface_longitude_name = ifnone(surface_longitude_name, df.columns[5])

        dataclass_obj = DirectionalSurvey(wellId=df[wellId_name][0],
                                          md=np.array(df[md_name]),
                                          inc=np.array(df[inc_name]),
                                          azim=np.array(df[azim_name]),
                                          surface_latitude=df[surface_latitude_name][0],
                                          surface_longitude=df[surface_longitude_name][0])
        return dataclass_obj