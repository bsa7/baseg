''' Этот файл содержит реализацию класса MongoClient '''
import pymongo
from app.lib.singleton import Singleton
from app.lib.env import Env

class MongoClient(metaclass = Singleton): # pragma: no cover
  ''' Этот класс реализует клиента для mongo db '''
  def __init__(self):
    self.client = pymongo.MongoClient(self.__connection_string)
    self.database = self.client[self.__mongo_database_name]
    self.collection = self.database['collection']

  def check_connection(self):
    ''' Проверяет соединение с mongodb '''
    return self.client.server_info()['version'] is not None

  @property
  def __connection_string(self):
    ''' Возвращает строку для соединения с сервисом '''
    return f"mongodb://{self.__auth_string}{self.__mongo_host}"

  @property
  def __auth_string(self) -> str:
    ''' Возвращает строку авторизации в сервисе MongoDB '''
    return f"{self.__mongo_user_name}:{self.__mongo_password}@"

  @property
  def __mongo_user_name(self) -> str:
    ''' Возвращает имя пользователя Mongo db '''
    return Env().get('MONGO_USER_NAME')

  @property
  def __mongo_password(self) -> str:
    ''' Возвращает пароль пользователя Mongo db '''
    return Env().get('MONGO_USER_PASSWORD')

  @property
  def __mongo_database_name(self) -> str:
    ''' Возвращает наименование бд mongo '''
    return Env().get('MONGO_DATABASE_NAME')

  @property
  def __mongo_host(self) -> str:
    ''' Возвращает имя хоста сервиса MongoDB '''
    return Env().get('MONGO_HOST')
