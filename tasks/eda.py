# Этот скрипт демонстрирует выполнение sql запроса в rdd
# Параметры скрипта:
#   * input_file - путь к parquet-файлу с историей пополнений
# Пример запуска:
# python -m tasks.eda input_file=../baseg-shared/data/wallet_urfu.parquet.gzip

import matplotlib.pyplot as plt
from app.lib.argument_parser import ArgumentParser
from app.lib.service_factory import ServiceFactory
from app.lib.parquet import Parquet

argument_parser = ArgumentParser()

# Парсим аргументы, переданные в командной строке
input_file_name = argument_parser.argument_safe('input_file', 'Ошибка! Вы должны указать имя файла с данными о пополнении баланса!')

spark = ServiceFactory().spark('SparkWithSQL')
df = Parquet().read_to_spark_df(input_file_name, spark)
df.createOrReplaceTempView('replenishments')

# Данный пример аггрегирует пополнения помесячно, для каждого клиента
# Для подсветки синтаксиса SQL в VSCode для python можно использовать расширение python-string-sql
result = spark.sql(f"""--beginsql
  SELECT
    partner AS client_id,
    CONCAT(CAST(YEAR(rep_date) AS STRING), '-', RIGHT(CONCAT('00', CAST(MONTH(rep_date) AS STRING)), 2)) AS rep_month,
    COUNT(monetary) AS operation_count
  FROM replenishments
   WHERE
     rep_date >= '2016-01-01'
     AND rep_date < '2023-12-31'
  GROUP BY
    client_id,
    rep_month
  ORDER BY
    client_id,
    rep_month
--endsql""")

print('Количества операций:')
result.show(100)
