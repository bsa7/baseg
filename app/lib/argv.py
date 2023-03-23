''' Этот файл содержит методы для работы с аргументами командной строки '''

class ArgumentParser:
  ''' Этот класс реализует методы разбора аргументов командной строки '''
  def __init__(self, argv):
    self.__argv = argv[1:]

  @property
  def ARGV(self):
    ''' Этот метод возвращает аргументы командной строки '''
    return self.__argv

  @property
  def arguments(self):
    ''' Этот метод возвращает именованные аргументы командной строки в виде словаря '''
    return dict([x.split('=') for x in self.ARGV])
