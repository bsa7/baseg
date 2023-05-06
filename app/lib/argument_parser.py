''' Этот файл содержит методы для работы с аргументами командной строки '''

import sys

class ArgumentParser:
  ''' Этот класс реализует методы разбора аргументов командной строки '''
  def __init__(self):
    self.__argv = sys.argv[1:]

  @property
  def ARGV(self):
    ''' Этот метод возвращает аргументы командной строки '''
    return self.__argv

  @property
  def arguments(self):
    ''' Этот метод возвращает именованные аргументы командной строки в виде словаря '''
    return dict([x.split('=') for x in self.ARGV])

  def argument_safe(self, argument_name: str, error_message: str = None, default = None):
    ''' Этот метод безопасно получает значение аргумента или райзит ошибку '''
    argument_value = self.arguments.get(argument_name)
    if error_message is not None and argument_value is None:
      raise ValueError(error_message)

    if argument_value is None and default is not None:
      argument_value = default

    return argument_value
