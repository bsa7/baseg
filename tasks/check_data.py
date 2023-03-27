''' Этот файл проверяет корректность данных в датасете '''
# Запуск: python -m tasks.check_data input_file=../baseg-shared/data/wallet_urfu.parquet.gzip batch_size=10000000
# batch_size - необязательный параметр - ограничение кол-ва строк

import pandas as pd
import pyarrow.parquet as pq
from app.lib.argument_parser import ArgumentParser
from pyarrow.parquet import ParquetFile
from pyarrow import Table as patb

argument_parser = ArgumentParser()
input_file_name = argument_parser.argument_safe('input_file',
                                                'Ошибка! Вы должны указать имя файла с данными о пополнении баланса!')
batch_size = argument_parser.argument_safe('batch_size')

# ---------Раскомментировать, чтобы брать только часть строк------------
pf = ParquetFile(input_file_name)
if batch_size is None:
  data = pd.read_parquet(input_file_name)
else:
  first_rows = next(pf.iter_batches(batch_size = int(batch_size)))  # Здесь можно задать количество первых n строк из паркета
  data = patb.from_batches([first_rows]).to_pandas()

# Проверяем, есть ли дублирующиеся строки
duplicateRows = data[data.duplicated()]
print("Дублированных строк:", duplicateRows.shape[0])

# Выводим есть ли нулевые значения
print("Строки с нулчевыми значениями есть? ", data.isnull().values.any())

# Переводим дату из строки в дату
data["rep_date_dt"] = pd.to_datetime(data["rep_date"])

# Отделяем год от даты
data["year"] = data["rep_date_dt"].apply(lambda x: x.year)

# Группируем по году и считаем кол-во
data.groupby(data["year"]).count()

print(data.groupby(data["year"]).count())
