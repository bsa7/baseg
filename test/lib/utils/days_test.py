''' Этот файл содержит тесты для app/lib/utils.py '''
import unittest
from app.lib.utils import days

class TestDays(unittest.TestCase):
  ''' Этот класс запускает тесты для метода days '''
  def test_days_returns_zero(self):
    ''' Этот тестовый случай проверяет нулевой результат для переданного нулевого временного штампа '''
    self.assertEqual(days(0), 0)

  def test_days_returns_for_integer_argument(self):
    ''' Этот тестовый случай проверяет результат для корректно переданного временного штампа '''
    self.assertEqual(days(11), 950400000)

  def test_days_returns_for_float_argument(self):
    ''' Этот тестовый случай проверяет результат для переданного значения временного штампа в виде значения с плавающей точкой '''
    self.assertEqual(days(1.45), 125280000)
