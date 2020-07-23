
# class DataObject(metaclass=abc.ABCMeta):
# @abc.abstractmethod
# def validate(self):
# pass
# def serialize(self):
# @dataclass
# class DeviationSurvey(DataObject):
# dls: np.array = field...
# class ClaculableObject(DataObject):
# @abc.abstractmethod
# def calculate(self, **kwargs):
# pass
# class DirectionalSurvey(ClaculableObject):
# my_dev_survey = DeviationSurvey().deserialize(json1) # get the path to the file
# pathfile = "data/json1.json"