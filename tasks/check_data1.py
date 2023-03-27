from app.lib.parquet import Parquet
from app.lib.service_factory import ServiceFactory
from app.lib.argument_parser import ArgumentParser
from pyspark.sql import functions as sql_functions

argument_parser = ArgumentParser()
input_file_name = argument_parser.argument_safe('input_file', 'Ошибка! Вы должны указать имя файла с данными о пополнении баланса!')

# Загружаем данные о пополнении баланса в датафрейм:
spark = ServiceFactory().spark('RMFCast')
df = Parquet().read_to_spark_df(input_file_name, spark) \
  .withColumnRenamed('partner', 'client_id') \
  .withColumn('year', sql_functions.year(sql_functions.col('rep_date'))) \
  .groupBy('year') \
  .agg(
    sql_functions.sum('monetary').alias('m'))


print(df.toPandas())

# Завершаем сессию Apache Spark
spark.stop()
