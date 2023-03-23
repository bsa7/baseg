# Этот скрипт загружает информацию о пополнениях баланса клиентами в Apache Spark дата фрейм
# На основании исходных данных составляется новый дата фрейм с признаками по клиентам:
# client_id; recency; frequency; monetary
# Параметры скрипта:
#   * input_file - путь к parquet-файлу с историей пополнений
#   * target_date - дата, на которую нужно посчитать метрики R, F, M. Формат даты = дд.мм.гггг
#   * output_file - путь к файлу, в который будет записан датафрейм с признаками.
# Пример запуска:
# Обратите внимание, что для файлов используется папка ../data - снаружи текущего репозитория
# python -m tasks.parquet_info_with_spark input_file=../data/data.parquet.gzip target_date=23.03.2023 output_file=../data/result.parquet

import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as sql_functions
from pyspark.sql.window import Window
from app.lib.argv import ArgumentParser

argument_parser = ArgumentParser(sys.argv)

print(f'{argument_parser.arguments=}')

# Парсим аргументы, переданные в командной строке
input_file_name = argument_parser.arguments.get('input_file')
if input_file_name is None:
  raise ValueError('Ошибка! Вы должны указать имя файла с данными о пополнении баланса!')

target_date = argument_parser.arguments.get('target_date')
if target_date is None:
  raise ValueError('Ошибка! Вы должны указать дату, на которую нужно найти признаки')

output_file_name = argument_parser.arguments.get('output_file')
if output_file_name is None:
  raise ValueError('Ошибка! Вы должны указать имя результирующего файла1')

print(f'=============== Обрабатывается файл {input_file_name} ===============')

# Загружаем данные о пополнении баланса в датафрейм:
spark = SparkSession.builder.appName('ParquetInfoWithSpark').getOrCreate()
df = spark.read.parquet(input_file_name) \
  .withColumnRenamed('partner', 'client_id')

# Для вычисления разности дат, добавляем колонку `date` к исходному датафрейму
df = df.withColumn('target_date', sql_functions.to_date(sql_functions.lit(target_date), 'dd.MM.yyyy'))

# Создаём датафрейм с признаком недавности (r), частоты (f) и денежности (m) клиента:
# r высчитана в днях, f - в количестве пополнений, m - в абстрактных еденицах суммы
recency_df = df.filter(df.rep_date <= df.target_date) \
  .withColumn('date_diff', sql_functions.datediff('target_date', 'rep_date')) \
  .groupBy('client_id') \
  .agg(
    sql_functions.min('date_diff').alias('r'), \
    sql_functions.count('date_diff').alias('f'), \
    sql_functions.sum('monetary').alias('m'))

recency_df.show(20)
print(f'Всего уникальных клиентов: {recency_df.count()}')
# Пишем результат в указанный файл output_file
recency_df.repartition(1).write.format('parquet').save(output_file_name)
# Завершаем сессию Apache Spark
spark.stop()
