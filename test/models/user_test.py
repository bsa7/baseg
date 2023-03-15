''' Этот файл содержит тесты для класса User '''
import unittest
from app.models.application_record import ApplicationRecord
from app.models.user import User
from app.models.wallet_replenishment import WalletReplenishment
from app.lib.utils import current_timestamp

class TestUser(unittest.TestCase):
  ''' Этот класс содержит тесты для модели User '''

  def setUp(self):
    ''' Очищает хранилище перед каждым тестом '''
    ApplicationRecord.collection.cleanup()

  def test_receive_empty_wallet_replenishments(self):
    ''' Проверяет получение пустого списка пополнения кошелька для пользователя '''
    user1 = User.insert_one(id = 123456)
    user2 = User.insert_one(id = 123457)
    WalletReplenishment.insert_one(user_id = 123456, rep_date = current_timestamp(), monetary = 100500)
    WalletReplenishment.insert_one(user_id = 123456, rep_date = current_timestamp(), monetary = 100)
    WalletReplenishment.insert_one(user_id = 123457, rep_date = current_timestamp(), monetary = 500)

    self.assertEqual(len(user1.wallet_replenishments()), 2)
    self.assertEqual(len(user2.wallet_replenishments()), 1)
