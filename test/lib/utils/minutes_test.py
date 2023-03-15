''' Этот файл содержит тесты для app/lib/utils.py '''
import unittest
from app.lib.utils import minutes

class TestMinutes(unittest.TestCase):
  ''' Этот класс запускает тесты для метода minutes '''
  def test_minutes_returns_zero(self):
    ''' Этот тестовый случай проверяет нулевой результат для переданного нулевого временного штампа '''
    self.assertEqual(minutes(0), 0)

  def test_minutes_returns_for_integer_argument(self):
    ''' Этот тестовый случай проверяет результат для корректно переданного временного штампа '''
    self.assertEqual(minutes(11), 660000)

  def test_minutes_returns_for_float_argument(self):
    ''' Этот тестовый случай проверяет результат для переданного значения временного штампа в виде значения с плавающей точкой '''
    self.assertEqual(minutes(1.45), 87000)
