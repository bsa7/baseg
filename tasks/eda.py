# Этот скрипт демонстрирует выполнение sql запроса в rdd
# Параметры скрипта:
#   * input_file - путь к parquet-файлу с историей пополнений
# Пример запуска:
# python -m tasks.eda input_file=../baseg-shared/data/wallet_urfu.parquet.gzip

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
# result = spark.sql(r"""
#   SELECT
#     max(rep_date) AS max_date,
#     min(rep_date) AS min_date
#   FROM replenishments
# """)

# print('Даты самого последнего и самого первого пополнений')
# result.show(1)

# Данный пример находит наибольшую и наименьшую суммы пополнений
# result = spark.sql(r"""
#   SELECT
#     max(monetary) AS max_replenishment,
#     min(monetary) AS min_replenishment
#   FROM replenishments
# """)


# print('Наибольшая и наименьшая суммы пополнений:')
# result.show(1)

# Данный пример аггрегирует пополнения помесячно, для каждого клиента
# Для подсветки синтаксиса SQL в VSCode для python можно использовать расширение python-string-sql
result = spark.sql(f"""--beginsql
  SELECT
    partner AS client_id,
    CONCAT(CAST(YEAR(rep_date) AS STRING), '-', RIGHT(CONCAT('00', CAST(MONTH(rep_date) AS STRING)), 2)) AS rep_month,
    SUM(monetary) AS monetary_per_month
  FROM replenishments
  WHERE
    rep_date >= '2017-03-01'
    AND rep_date < '2018-03-01'
  GROUP BY
    rep_month,
    client_id
  ORDER BY
    monetary_per_month DESC
--endsql""")

print('Аггрегированные суммы пополнений:')
result.show(10)
