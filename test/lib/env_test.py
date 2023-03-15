''' Этот файл содержит тесты для app/lib/env.py '''
import unittest
import os
from app.lib.env import Env

class TestEnv(unittest.TestCase):
  ''' Этот класс запускает тесты для класса Env '''
  def test_get_existed_environment_variable(self):
    ''' Этот тестовый случай проверяет, что Env.get может правильно прочитать значение переменной окружения. '''
    expected_value = 'something'
    var_name = 'TEST_VARIABLE'
    os.environ[var_name] = expected_value
    self.assertEqual(Env().get(var_name), expected_value)
    os.environ.pop(var_name, None)

  def test_get_unexisted_environment_variable(self):
    ''' Этот тестовый случай проверяет, что Env.get корректно читает значение несуществующей переменной окружения '''
    expected_value = None
    var_name = 'TEST_VARIABLE'
    self.assertEqual(Env().get(var_name), expected_value)

  def test_get_env_name(self):
    ''' Этот тестовый случай проверяет, что Env.name возвращает правильное наименование окружения '''
    expected_env_name = 'test'
    self.assertEqual(Env().name, expected_env_name)
