''' Этот файл содержит тесты для app/lib/utils.py '''
import unittest
from app.lib.utils import seconds

class TestSeconds(unittest.TestCase):
  ''' Этот класс запускает тесты для метода seconds '''
  def test_seconds_returns_zero(self):
    ''' Этот тестовый случай проверяет нулевой результат для переданного нулевого временного штампа '''
    self.assertEqual(seconds(0), 0)

  def test_seconds_returns_for_integer_argument(self):
    ''' Этот тестовый случай проверяет результат для корректно переданного временного штампа '''
    self.assertEqual(seconds(11), 11000)

  def test_seconds_returns_for_float_argument(self):
    ''' Этот тестовый случай проверяет результат для переданного значения временного штампа в виде значения с плавающей точкой '''
    self.assertEqual(seconds(1.45), 1450)
