''' Этот файл содержит самодельную реализацию эмуляции клиента mongodb '''
from app.lib.test.collection import Collection

class MongoClient:
  ''' Этот класс реализует тестировочный клиент для MongoDB '''
  collection = Collection
