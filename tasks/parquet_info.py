''' Этот файл содержит код, который выдаёт инфу по parquet-файлу с данными '''
# Для запуска нужно указать местоположение parquet-файла с данными
# Например: python ./tasks/parquet_info.py ../baseg-shared/data/wallet_urfu.parquet.gzip
import sys
import pyarrow.parquet as pq

if len(sys.argv) < 2:
  raise ValueError('Ошибка! Вы должны указать имя файла первым аргументом!')

file_name = sys.argv[1]

print(f'=============== Файл {file_name} ===============')

table = pq.read_table(file_name)
schema = table.schema
print(f'{schema=}')

df = table.to_pandas()
print(f'{df.head()=}')
print(f'{df.tail()=}')
