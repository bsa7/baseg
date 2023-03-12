''' Это временный файл для инициализации тестов '''

import unittest
from app.lib.hello_world import HelloWorld

class TestHelloWorld(unittest.TestCase):
  ''' Этот класс якобы что то тестирует '''
  def test_check(self):
    ''' This case checks the result for a valid zero timestamp '''
    result = HelloWorld().check()
    self.assertEqual(result, 1)
