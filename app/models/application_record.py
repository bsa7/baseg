''' This file contains ApplicationRecord abstract class definition '''
from app.lib.service_factory import ServiceFactory

class ApplicationRecord():
  ''' This abstract class contains base methods for data operation in mongo db '''
  collection = ServiceFactory().mongo_client().collection

  def __init__(self, document = None):
    ''' Initializes instance '''
    self.__document = document

  @property
  def id(self):
    ''' Возвращает содержимое атрибута "id" mongo документа '''
    return self.__document.get('id')

  def get(self, attr_name: str):
    ''' Возвращает значение атрибута документа '''
    return self.__document.get(attr_name)

  @classmethod
  def count(cls, **filter_attributes) -> int:
    ''' Returns count of model's records '''
    return cls.collection.count_documents({ 'model': cls.__name__, **filter_attributes })

  @classmethod
  def find_one(cls, **attributes):
    ''' find record by filter '''
    result = cls.collection.find_one({ 'model': cls.__name__, **attributes })
    if result is not None:
      return cls(result)

    return None

  @classmethod
  def insert_one(cls, **record_attributes):
    ''' Insert one record model's records '''
    cls.collection.insert_one({ 'model': cls.__name__, **record_attributes })
    return cls.find_one(**record_attributes)

  @classmethod
  def upsert_one(cls, find_by, data):
    ''' Update existed or create new record '''
    existed_item = cls.find_one(**find_by)
    if existed_item is None:
      return cls.insert_one(**find_by, **data)

    return cls.collection.update_one({ 'model': cls.__name__, **find_by }, { '$set': data })

  @classmethod
  def where(cls, **filter_attributes):
    ''' Returns records by filter_attributes '''
    return cls.collection.find({ 'model': cls.__name__, **filter_attributes })

  @classmethod
  def unset_many(cls, filter_attributes, unset_attributes):
    ''' Unset multiple keys in filtered records '''
    return cls.collection.update_many(filter_attributes, { '$unset': unset_attributes })
