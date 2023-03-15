''' Этот файл содержит тесты для app/lib/utils.py '''
import unittest
from app.lib.utils import timestamp_to_formatted_datetime

class TestTimestampToFormattedDatetime(unittest.TestCase):
  ''' Этот класс запускает тесты для метода timestamp_to_formatted_datetime '''
  def test_result_with_valid_parameter(self):
    ''' Этот тестовый случай проверяет результат для правильно переданного временного штампа '''
    self.assertEqual(timestamp_to_formatted_datetime(1585557000231), '2020-03-30 08:30:00.231000')

  def test_result_when_parameter_is_none(self):
    ''' Этот тестовый случай проверяет возникновение ошибки в случае, если временной штамп не передан '''
    self.assertRaises(TypeError, lambda: timestamp_to_formatted_datetime(None))

  def test_result_with_wrong_parameter(self):
    ''' Этот тестовый случай проверяет возникновение ошибки, если передан некоррентный временной штамп '''
    self.assertRaises(ValueError, lambda: timestamp_to_formatted_datetime(1585557000231121))
