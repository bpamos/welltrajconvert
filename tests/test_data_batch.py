# import unittest
# from src.data_batch import *
#
# class TestDataBatch(unittest.TestCase):
#     def test_data_batch_normal(self):
#         current_dir = Path.cwd()
#         path = current_dir.parent / 'data'
#         file_path = path / 'wellbore_survey.csv'
#
#         df = pd.read_csv(file_path, sep=',')
#         df = df[['wellId', 'md', 'inc', 'azim', 'surface_latitude', 'surface_longitude']]
#
#         my_data = DataBatch(df)
#         my_df = my_data.from_df()
#         #my_df.wellId
#
#         self.assertEqual(len([my_df.wellId]), 1, 'incorrect')
#
#
#     def test_data_batch_new_col(self):
#         current_dir = Path.cwd()
#         path = current_dir.parent / 'data'
#         file_path = path / 'wellbore_survey.csv'
#
#         df = pd.read_csv(file_path, sep=',')
#         df = df[['wellId', 'md', 'inc', 'azim', 'surface_latitude', 'surface_longitude']]
#
#         df.rename(columns={'wellId': 'UWI', 'md': 'MD',
#                            'inc': 'Inclination', 'azim': 'Azimuth'}, inplace=True)
#         df = df.iloc[:, ::-1]
#
#         my_data = DataBatch(df)
#         my_df = my_data.from_df(wellId_name='UWI', md_name='MD', inc_name='Inclination',
#                                 azim_name='Azimuth', surface_latitude_name='surface_latitude',
#                                 surface_longitude_name='surface_longitude')
#
#         self.assertEqual(len([my_df.wellId]), 1, 'incorrect')
#
#
#
#     def test_from_df_and_header_values(self):
#         current_dir = Path.cwd()
#         path = current_dir.parent / 'data'
#         file_path = path / 'wellbore_survey.csv'
#
#         df = pd.read_csv(file_path, sep=',')
#         df = df[['md', 'inc', 'azim']]
#
#         my_data = DataBatch(df)
#         my_df = my_data.from_df_and_header_values()
#
#         my_df = my_data.from_df_and_header_values(wellId_val='my_new_well', surface_latitude_val=23.,
#                                                 surface_longitude_val=56.)
#
#
#         self.assertEqual(len([my_df.wellId]), 1, 'incorrect')
#
#
#
#
#
# if __name__ == '__main__':
#     unittest.main()
