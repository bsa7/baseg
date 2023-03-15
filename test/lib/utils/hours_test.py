''' Этот файл содержит тесты для app/lib/utils.py '''
import unittest
from app.lib.utils import hours

class TestHours(unittest.TestCase):
  ''' Этот класс запускает тесты для метода hours '''
  def test_hours_returns_zero(self):
    ''' Этот тестовый случай проверяет нулевой результат для переданного нулевого временного штампа '''
    self.assertEqual(hours(0), 0)

  def test_hours_returns_for_integer_argument(self):
    ''' Этот тестовый случай проверяет результат для корректно переданного временного штампа '''
    self.assertEqual(hours(11), 39600000)

  def test_hours_returns_for_float_argument(self):
    ''' Этот тестовый случай проверяет результат для переданного значения временного штампа в виде значения с плавающей точкой '''
    self.assertEqual(hours(1.45), 5220000)
