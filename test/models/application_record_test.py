''' Этот файл содержит тесты для абстрактного класса ApplicationRecord, реализуемые через наследуемый класс User '''
import unittest
from app.models.application_record import ApplicationRecord
from app.models.user import User
from test.support.assert_helper import assert_record_contain_values

class TestApplicationRecord(unittest.TestCase):
  ''' Этот класс содержит тесты для базового функционала модели данных.
      В данном случае она реализована на основе User::ApplicationRecord класса'''

  def setUp(self):
    ''' Очищает хранилище перед каждым тестом '''
    ApplicationRecord.collection.cleanup()

  def test_zero_count(self):
    ''' Проверяет, что модель корректно сообщает количество записей, если записей нет '''
    count = User.count()
    self.assertEqual(count, 0)

  def test_count(self):
    ''' Проверяет, что модель корректно возвращает правильное число записей '''
    User.insert_one(id = 123456)
    User.insert_one(id = 123457)
    self.assertEqual(User.count(), 2)

  def test_insert_one(self):
    ''' Проверяем, что модель вставляет запись в хранилище '''
    record_search_attributes = { 'id': 12345 }
    record_attributes = { 'y': 123 }
    expected_record_attributes = { **record_search_attributes, **record_attributes }
    User.insert_one(**record_search_attributes, **record_attributes)
    created_record = User.find_one(**record_search_attributes)
    assert_record_contain_values(created_record, expected_record_attributes, comparator = self.assertEqual)

  def test_upsert_one_when_no_record_exist(self):
    ''' Проверяет, что модель корректно создаёт новую запись, если существующая не найдена '''
    record_search_attributes = { 'id': 12345 }
    record_attributes = { 'y': 123 }
    expected_record_attributes = { **record_search_attributes, **record_attributes }
    existed_record = User.find_one(**record_search_attributes)
    self.assertEqual(existed_record, None)
    User.upsert_one(find_by = record_search_attributes, data = record_attributes)
    created_record = User.find_one(**record_search_attributes)
    assert_record_contain_values(created_record, expected_record_attributes, comparator = self.assertEqual)

  def test_upsert_one_when_same_record_exist(self):
    ''' Проверяет, что модель корректно обновляет запись, если такая уже существует '''
    record_search_attributes = { 'id': 12345 }
    record_attributes = { 'y': 123 }
    new_record_attributes = { 'y': 125 }
    expected_existed_record_attributes = { **record_search_attributes, **record_attributes }
    expected_updated_record_attributes = { **record_search_attributes, **new_record_attributes }
    User.insert_one(**record_search_attributes, **record_attributes)
    existed_record = User.find_one(**record_search_attributes)
    assert_record_contain_values(existed_record, expected_existed_record_attributes, comparator = self.assertEqual)
    User.upsert_one(find_by = record_search_attributes, data = new_record_attributes)
    created_record = User.find_one(**record_search_attributes)
    assert_record_contain_values(created_record, expected_updated_record_attributes, comparator = self.assertEqual)

  def test_unset_many(self):
    ''' Проверяет, что модель корректно удаляет атрибуты в существующих записях '''
    record_search_attributes = { 'id': 12345 }
    User.insert_one(**record_search_attributes, key1 = 1, key2 = 2)
    User.insert_one(ds = 12346, key1 = 1, key2 = 2)
    existed_record = User.find_one(**record_search_attributes)
    self.assertEqual(existed_record.get('key2'), 2)
    User.unset_many(filter_attributes = record_search_attributes, unset_attributes = { 'key2': 1 })
    existed_record = User.find_one(**record_search_attributes)
    self.assertEqual(existed_record.get('key2'), None)
