''' Этот файл содержит тесты для класса Parquet '''
import unittest

from app.lib.service_factory import ServiceFactory
from app.lib.parquet import Parquet

class TestParquet(unittest.TestCase):
  ''' Этот класс запускает тесты Parquet '''
  def setUp(self):
    self.__spark = ServiceFactory().spark('testParquet')

  def test_read_to_spark_df(self):
    ''' Этот тестовый случай проверяет, что метод read_to_spark_df корректно читает parquet файл '''
    file_name = './test/fixtures/test_df.parquet.gzip'
    expected_columns = ['col1', 'col2']
    df = Parquet().read_to_spark_df(file_name, self.__spark)
    self.assertEqual(df.columns, expected_columns)
