''' Этот файл содержит определение класса Env '''
import os
from dotenv import load_dotenv
from app.lib.singleton import Singleton

class Env(metaclass = Singleton):
  ''' Этот класс реализует методы для чтения переменных среды '''
  def __init__(self):
    load_dotenv()

  def get(self, variable_name: str):
    ''' Этот метод читает значение переменной среды '''
    return os.getenv(variable_name)

  @property
  def name(self) -> str:
    ''' Этот метод возвращает имя окружения (test | development | production) '''
    return os.getenv('PYTHON_ENV')
