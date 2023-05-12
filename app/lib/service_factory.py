''' Этот файл содержит определение класса ServiceFactory '''
from pyspark.sql import SparkSession
from app.lib.singleton import Singleton
from app.lib.env import Env
from app.lib.mongo_client import MongoClient
from app.lib.test.mongo_client import MongoClient as TestMongoClient

class ServiceFactory(metaclass = Singleton):
  ''' Этот класс производит классы клиентов для подключения к различным сервисам  '''
  @property
  def mongo_client(self):
    ''' Этот метод возвращает класс для клиента MongoDB '''
    return self.__client_by_env_name(production = MongoClient, test = TestMongoClient)

  def spark(self, app_name):
    ''' Этот метод возвращает сессию Apache Spark '''
    return SparkSession.\
      builder. \
      appName(app_name). \
      config('spark.executor.memory', '10g'). \
      config('spark.driver.memory', '10g'). \
      getOrCreate()

  # Приватные методы класса

  def __client_by_env_name(self, development = None, production = None, test = None):
    ''' Этот метод возвращает один из предложенных вариантов классов, в зависимости от текущего окружения '''
    env_name = Env().name
    print(f'{env_name=}')
    if env_name == 'test':
      return test or development or production

    if env_name == 'development': # pragma: no cover
      return development or production

    return production or development # pragma: no cover
