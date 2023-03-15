''' Этот файл содержит тесты для app/lib/utils.py '''
import unittest
from datetime import datetime
from app.lib.utils import current_timestamp

class TestCurrentTimestamp(unittest.TestCase):
  ''' Этот класс запускает тесты для метода current_timestamp '''
  def test_current_timestamp_returns_current_time(self):
    ''' Этот тестовый случай проверяет результат для правильно переданного штампа времени '''
    expected_timestamp = int(datetime.now().timestamp() * 1000)
    self.assertEqual(current_timestamp(), expected_timestamp)
