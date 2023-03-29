# Этот скрипт демонстрирует выполнение sql запроса в rdd
# Параметры скрипта:
#   * input_file - путь к parquet-файлу с историей пополнений
# Пример запуска:
# python -m tasks.eda input_file=../baseg-shared/data/wallet_urfu.parquet.gzip

import pdb
from app.lib.argument_parser import ArgumentParser
from app.lib.service_factory import ServiceFactory
from app.lib.parquet import Parquet

argument_parser = ArgumentParser()

# Парсим аргументы, переданные в командной строке
input_file_name = argument_parser.argument_safe('input_file', 'Ошибка! Вы должны указать имя файла с данными о пополнении баланса!')

spark = ServiceFactory().spark('SparkWithSQL')
df = Parquet().read_to_spark_df(input_file_name, spark)
df.createOrReplaceTempView('replenishments')

# Данный пример находит даты самого первого и самого последнего пополнений
result = spark.sql(r"""
  SELECT
    max(rep_date) AS max_date,
    min(rep_date) AS min_date
  FROM replenishments
""")

print('Даты самого последнего и самого первого пополнений')
result.show(1)

# Данный пример находит наибольшую и наименьшую суммы пополнений
result = spark.sql(r"""
  SELECT
    max(monetary) AS max_replenishment,
    min(monetary) AS min_replenishment
  FROM replenishments
""")

print('Наибольшая и наименьшая суммы пополнений:')
result.show(1)
