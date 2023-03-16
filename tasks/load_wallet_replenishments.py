''' Этот файл содержит выполняет загрузку пополнений кошельков пользователей в mongodb '''
# Для запуска нужно указать местоположение parquet-файла с данными
# Например: python ./tasks/load_wallet_replenishments.py ../baseg-shared/data/wallet_urfu.parquet.gzip
import sys
import pdb
import pyarrow.parquet as pq
from app.models.user import User
from app.models.wallet_replenishment import WalletReplenishment

if len(sys.argv) < 2:
  raise ValueError('Ошибка! Вы должны указать имя файла первым аргументом!')

file_name = sys.argv[1]
table = pq.read_table(file_name)
rows_count = table.num_rows

parquet_file = pq.ParquetFile(file_name)

def converter(row):
  date = str(row['rep_date'])
  result = {
    '_id': f"{row['partner']}-{date}",
    'user_id': row['partner'],
    'date': date,
    'monetary': row['monetary'],
  }
  return result

pdb.set_trace()
a = 1 / 0
total_readed = 0
WalletReplenishment.collection.drop()
user_ids = set()
for batch in parquet_file.iter_batches():
  total_readed += len(batch)
  wallet_replenishments = map(converter, batch.to_pylist())
  user_ids.update([user_id.as_py() for user_id in set(batch[0])])
  WalletReplenishment.insert_many(wallet_replenishments)
  sys.stdout.write(f'\rИдёт загрузка записей: {round(total_readed / rows_count * 100, 2)}% готово.')
  sys.stdout.flush()

users = [{ '_id': id } for id in user_ids]
User.insert_many(users)
