''' Этот файл содержит выполняет загрузку уникальных пользователей в mongodb '''
# Для запуска нужно указать местоположение parquet-файла с данными
# Например: python ./tasks/load_users.py ../baseg-shared/data/wallet_urfu.parquet.gzip
import sys
import pyarrow.parquet as pq
from app.models.user import User

if len(sys.argv) < 2:
  raise ValueError('Ошибка! Вы должны указать имя файла первым аргументом!')

file_name = sys.argv[1]
table = pq.read_table(file_name)
rows_count = table.num_rows

parquet_file = pq.ParquetFile(file_name)

total_readed = 0

def show_status(total_readed, rows_count, users_count):
  sys.stdout.write(f'\rИдёт загрузка записей: {round(total_readed / rows_count * 100, 2)}% готово. Всего найдено {users_count} уникальных пользователей.')
  sys.stdout.flush()


User.collection.drop()
user_ids = set()
for batch in parquet_file.iter_batches():
  total_readed += len(batch)
  user_ids.update([user_id.as_py() for user_id in set(batch[0])])
  show_status(total_readed, rows_count, len(user_ids))

users = [{ '_id': id } for id in user_ids]
User.insert_many(users)
