''' Этот файл содержит тесты для парсера аргументов командной строки '''
import unittest
from unittest.mock import patch
from app.lib.argument_parser import ArgumentParser

class TestArgumentParser(unittest.TestCase):
  ''' Этот класс содержит тесты ArgumentParser '''
  def test_ARGV(self):
    ''' Этот тестовый случай проверяет чтение аргументов командной строки '''
    argv = self.__argument_parser('filename.py param1=aaa param2=bbb').ARGV
    self.assertEqual(argv, ['param1=aaa', 'param2=bbb'])

  def test_arguments(self):
    ''' Этот тестовый случай проверяет получение аргументов в виде словаря '''
    arguments = self.__argument_parser('filename.py param1=aaa param2=bbb').arguments
    self.assertEqual(arguments, { 'param1': 'aaa', 'param2': 'bbb' })

  def test_argument_safe_when_parameter_present(self):
    ''' Этот тестовый случай проверяет получение аргумента по имени, если аргумент представлен '''
    argument_parser = self.__argument_parser('filename.py param1=aaa param2=bbb')
    argument_value = argument_parser.argument_safe('param1', 'error message')
    self.assertEqual(argument_value, 'aaa')

  def test_argument_safe_when_parameter_absent(self):
    ''' Этот тестовый случай проверяет получение аргумента по имени, если аргумент не представлен '''
    argument_parser = self.__argument_parser('filename.py param1=aaa param2=bbb')
    expected_error_message = 'error message'
    with self.assertRaisesRegex(ValueError, expected_error_message):
      _ = argument_parser.argument_safe('param3', expected_error_message)

  def __argument_parser(self, arguments: str):
    with patch('sys.argv', arguments.split(' ')):
      return ArgumentParser()
