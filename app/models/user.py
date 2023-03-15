''' Этот файл содержит определение для модели User '''
from app.models.application_record import ApplicationRecord
from app.models.wallet_replenishment import WalletReplenishment

class User(ApplicationRecord):
  ''' Этот класс содержит определение модели Пользователь '''
  def wallet_replenishments(self):
    ''' Возвращает историю пополнений кошелька для данного пользователя '''
    return WalletReplenishment.where(user_id = self.id)
