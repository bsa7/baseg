''' Этот файл содержит тесты для класса MongoClient '''
import unittest
from app.lib.service_factory import ServiceFactory

class TestMongoClient(unittest.TestCase):
  ''' Этот класс запускает тесты Mongo клиента '''
  def setUp(self):
    self.__collection = ServiceFactory().mongo_client().collection

  def test_insert_one(self):
    ''' Этот тестовый случай проверяет, что монго клиент вставляет запись в коллекцию '''
    expected_document = { '_id': 'id-100500' }
    self.__collection.insert_one(expected_document)
    result = self.__collection.find_one(expected_document)
    self.assertEqual(expected_document, result)
